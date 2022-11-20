import os

from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram.ext import PicklePersistence

from helpers.logger import create_logger

from conversations.add_account import add_account_handler
from commands import available_commands, currency, start, my_accounts


logger = create_logger('root')


if __name__ == '__main__':
    my_persistence = PicklePersistence(filepath='persistent_data/data.pickle')
    application = ApplicationBuilder().token(os.environ['TOKEN']).persistence(persistence=my_persistence).build()

    start_handler = CommandHandler('start', start.start_command)
    application.add_handler(start_handler)

    available_commands_handler = CommandHandler('commands', available_commands.available_commands_command)
    application.add_handler(available_commands_handler)

    application.add_handler(add_account_handler)

    my_accounts_handler = CommandHandler('my_accounts', my_accounts.my_accounts_command)
    application.add_handler(my_accounts_handler)

    currency_handler = CommandHandler('currency', currency.currency_command)
    application.add_handler(currency_handler)

    application.run_polling()
