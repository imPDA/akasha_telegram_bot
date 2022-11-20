from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.from_user.id)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Это твой личный терминал Акаши!! С его помощью можно делать много крутых штук! "
             "/commands - узнать обо всех возможностях."
    )
