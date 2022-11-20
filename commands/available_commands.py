from telegram import Update
from telegram.ext import ContextTypes


async def available_commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="- С помощью бота можно отслеживать свои текущие примогемы и монеты в чайнике. Чтобы это сделать, "
             "нужно добавить токен с сайта HoYoLAB. Инструкция: https://google.com. "
             "Команда для добавления: /add_account."
    )
