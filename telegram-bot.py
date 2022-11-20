import os
import genshin

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from telegram.ext import filters
from telegram.ext import PicklePersistence

from helpers.logger import create_logger


logger = create_logger('root')

UID, LTUID, LTOKEN = range(3)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Это твой личный терминал Акаши!! С его помощью можно делать много крутых штук! "
             "/commands - узнать обо всех возможностях."
    )


async def available_commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="- С помощью бота можно отслеживать свои текущие примогемы и монеты в чайнике. Чтобы это сделать, "
             "нужно добавить токен с сайта HoYoLAB. Инструкция: https://google.com. "
             "Команда для добавления: /add_account."
    )


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


async def my_accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Твои добавленные UID: {', '.join(context.user_data['genshin_account'].keys())}"
    )


async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for account in context.user_data['genshin_account'].values():
        ltuid = account['ltuid']
        ltoken = account['ltoken']

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


if __name__ == '__main__':
    my_persistence = PicklePersistence(filepath='persistent_data/data.pickle')
    application = ApplicationBuilder().token(os.environ['TOKEN']).persistence(persistence=my_persistence).build()

    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)

    available_commands_handler = CommandHandler('commands', available_commands_command)
    application.add_handler(available_commands_handler)

    add_account_handler = ConversationHandler(
        entry_points=[CommandHandler('add_account', add_account_command)],
        states={
            UID: [MessageHandler(filters.Regex("^\d{8,10}$"), uid_message_handler)],  # TODO better regex
            LTUID: [MessageHandler(filters.Regex("^\d{8}$"), ltuid_message_handler)],
            LTOKEN: [MessageHandler(filters.Regex("^[a-zA-Z\d]{40}$"), ltoken_message_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel_command)]
    )
    application.add_handler(add_account_handler)

    my_accounts_handler = CommandHandler('my_accounts', my_accounts_command)
    application.add_handler(my_accounts_handler)

    currency_handler = CommandHandler('currency', currency_command)
    application.add_handler(currency_handler)

    application.run_polling()
