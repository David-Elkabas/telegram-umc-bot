from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

from setting import TELEGRAM_BOT_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Staring Bot...')

logger = logging.getLogger(__name__)


def start_command(update, context):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')

def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User({update.message.chat.id}) says: {text}')

    # bot response
    update.message.reply_text(text)

def error(update, context):
    # log errors
    logging.error(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher

    # Commands
    dispatcher.add_handler(CommandHandler('start', start_command))

    # Messages
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dispatcher.add_error_handler(error)

    # Run the bot - checking new data each second
    updater.start_polling(1.0)
    updater.idle()


if __name__ == '__main__':
    main()
