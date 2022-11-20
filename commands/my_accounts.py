from telegram import Update
from telegram.ext import ContextTypes


async def my_accounts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Твои добавленные UID: {', '.join(context.user_data['genshin_account'].keys())}"
    )
