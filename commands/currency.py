import genshin
from telegram import Update
from telegram.ext import ContextTypes


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
                 f'({notes.remaining_realm_currency_recovery_time})'
        )
