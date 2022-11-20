import genshin

from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, ContextTypes, filters

UID, LTUID, LTOKEN = range(3)


async def add_account_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Введи UID (обычно 9 цифр)")
    return UID


async def uid_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['new_uid'] = update.message.text
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Введи ltuid (8 цифр)")
    return LTUID


async def ltuid_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if uid := context.user_data['new_uid']:
        context.user_data.setdefault('genshin_account', {}).setdefault(uid, {})['ltuid'] = int(update.message.text)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Введи ltoken (40 символов, букв и цифр)")
    return LTOKEN


async def rerun_resin(context: ContextTypes.DEFAULT_TYPE):
    uid = context.job.data['uid']
    ltuid = context.job.data['ltuid']
    ltoken = context.job.data['ltoken']

    client = genshin.Client(
        {
            'ltuid': ltuid,
            'ltoken': ltoken,
        }
    )

    notes = await client.get_notes()

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f'{notes.current_resin}/{notes.max_resin} resin ({notes.remaining_resin_recovery_time})\n'
             f'{notes.current_realm_currency}/{notes.max_realm_currency} coins '
             f'({notes.remaining_realm_currency_recovery_time})')

    timer = min(notes.remaining_resin_recovery_time.seconds, notes.remaining_realm_currency_recovery_time.seconds) \
        if all([notes.remaining_resin_recovery_time.seconds, notes.remaining_realm_currency_recovery_time.seconds]) \
        else max(notes.remaining_resin_recovery_time.seconds, notes.remaining_realm_currency_recovery_time.seconds)

    context.job_queue.run_once(
        rerun_resin,
        timer,
        chat_id=context.job.chat_id,
        data={'uid': uid, 'ltuid': ltuid, 'ltoken': ltoken}
    )


async def ltoken_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if uid := context.user_data['new_uid']:
        context.user_data.setdefault('genshin_account', {}).setdefault(uid, {})['ltoken'] = update.message.text

    ltuid = context.user_data['genshin_account'][uid]['ltuid']
    ltoken = context.user_data['genshin_account'][uid]['ltoken']

    client = genshin.Client(
        {
            'ltuid': ltuid,
            'ltoken': ltoken,
        }
    )

    notes = await client.get_notes()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'{notes.current_resin}/{notes.max_resin} resin ({notes.remaining_resin_recovery_time})\n'
             f'{notes.current_realm_currency}/{notes.max_realm_currency} coins '
             f'({notes.remaining_realm_currency_recovery_time})')

    context.job_queue.run_once(
        rerun_resin,
        60,
        chat_id=update.effective_chat.id,
        data={'uid': uid, 'ltuid': ltuid, 'ltoken': ltoken},
    )

    return ConversationHandler.END


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ...


add_account_handler = ConversationHandler(
        entry_points=[CommandHandler('add_account', add_account_command)],
        states={
            UID: [MessageHandler(filters.Regex("^\d{8,10}$"), uid_message_handler)],  # TODO better regex
            LTUID: [MessageHandler(filters.Regex("^\d{8}$"), ltuid_message_handler)],
            LTOKEN: [MessageHandler(filters.Regex("^[a-zA-Z\d]{40}$"), ltoken_message_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
