from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging
from typing import Dict

# import UC_coversation

from setting import TELEGRAM_BOT_TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Staring Bot...')

logger = logging.getLogger(__name__)


FIRST_CHOOSING, UC_QUESTIONS, ROIP_QUESTIONS, UMC_QUESTIONS, RETURN_TO_START = range(5)

reply_keyboard = [
    ['UC'],
    ['ROIP'],
    ['UMC'],]
first_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

uc_reply_keyboard = [
    ['טלפוניה'],
    ['כריזה'],
    ['ROOMKIT'],
    ['חזרה להתחלה'], ]
uc_markup = ReplyKeyboardMarkup(uc_reply_keyboard, one_time_keyboard=True)

roip_reply_keyboard = [
    ['גרסה 2.2.2'],
    ['גרסה 3.0'],
    ['גרסה 3.1'],
    ['חזרה להתחלה'], ]
roip_markup = ReplyKeyboardMarkup(roip_reply_keyboard, one_time_keyboard=True)

umc_reply_keyboard = [
    ['ואללה אין פה הרבה'],
    ['חזרה להתחלה'], ]
umc_markup = ReplyKeyboardMarkup(umc_reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} - {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def umc_first_selection(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    # text = update.message.text
    # context.user_data['choice'] = text
    update.message.reply_text("למה לחצת פה? אין פה כלום",
        reply_markup=umc_markup)
    return UMC_QUESTIONS


def roip_first_selection(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    # text = update.message.text
    # context.user_data['choice'] = text
    update.message.reply_text("אחלה בואו נצלול אל עולמות ה ROIP")
    update.message.reply_text("מה היא הגרסה עליה נרצה לדבר?",
        reply_markup=roip_markup)
    return ROIP_QUESTIONS


def uc_first_selection(update: Update, context: CallbackContext) -> int:
    """Ask the user for info about the selected predefined choice."""
    # text = update.message.text
    # context.user_data['choice'] = text
    # update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')
    update.message.reply_text("אחלה בואו נצלול אל עולמות הUC",
        reply_markup=uc_markup)
    return UC_QUESTIONS


def custom_choice(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom category."""
    update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )
    return TYPING_CHOICE


def received_information(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


def done(update: Update, context: CallbackContext) -> int:

    update.message.reply_text(
        f"יאלללללה בוא נתחיל מההתחלה",
        reply_markup = first_markup)

    return FIRST_CHOOSING


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def start_command(update, context: CallbackContext)-> int:
    """Start the conversation and ask user for input."""
    update.message.reply_text(
        "שלום לכל, וברוכים הבאים בלה בלה בלה תבחרו את הנושא המבוקש ותקבלו מענה",
        reply_markup=first_markup)

    return FIRST_CHOOSING


def error(update, context):
    # log errors
    logging.error(f'Update {update} caused error {context.error}')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Commands
    # dispatcher.add_handler(CommandHandler('start', start_command))

    # Messages
    # dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            FIRST_CHOOSING: [
                MessageHandler(Filters.regex('^UC$'), uc_first_selection),
                MessageHandler(Filters.regex('^ROIP$'), roip_first_selection),
                MessageHandler(Filters.regex('^UMC$'), umc_first_selection),
            ],
            UC_QUESTIONS: [
                MessageHandler(Filters.regex('^טלפוניה$'), custom_choice),
                MessageHandler(Filters.regex('^כריזה$'), custom_choice),
                MessageHandler(Filters.regex('^ROOMKIT$'), custom_choice),
                MessageHandler(Filters.regex('^חזרה להתחלה$'), done)
            ],
            ROIP_QUESTIONS: [
                MessageHandler(Filters.regex('^גרסה 2.2.2$'), custom_choice),
                MessageHandler(Filters.regex('^גרסה 3.0$'), custom_choice),
                MessageHandler(Filters.regex('^גרסה 3.1$'), custom_choice),
                MessageHandler(Filters.regex('^חזרה להתחלה$'), done)
            ],
            UMC_QUESTIONS:[MessageHandler(Filters.regex('^ואללה אין פה הרבה'), custom_choice),
                           MessageHandler(Filters.regex('^חזרה להתחלה$'), done)]
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Log all errors
    dispatcher.add_error_handler(error)

    # Run the bot - checking new data each second
    updater.start_polling(1.0)
    updater.idle()


if __name__ == '__main__':
    main()
