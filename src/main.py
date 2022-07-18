import os
import dotenv
import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler, MessageHandler, Filters)
from src.components import start, register, main_menu, settings, group, booking
from src import constants
from utils.db import check_db_exists
from utils.text import button
from utils.filter import multibuttons, ReplyToMessageFilter, FilterDateTimeButtons


dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)

logging.basicConfig(
    filename='logs.log' if not DEBUG else None,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO if not DEBUG else logging.DEBUG
)

logger = logging.getLogger(__name__)


def main():
    if not check_db_exists():
        raise Exception('Database not found!')

    updater = Updater(os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher

    main_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start.start)
        ],
        states={
            "REQUEST_NAME": [
                MessageHandler(Filters.text, register.get_name)
            ],
            "REQUEST_PHONE": [
                MessageHandler(Filters.text | Filters.contact,
                               register.get_phone)
            ],
            "REQUEST_LEVEL": [
                MessageHandler(Filters.regex(
                    multibuttons('levels')), register.get_level)
            ],
            "MAIN_MENU": [
                MessageHandler(Filters.regex(
                    button('book_session')), booking.get_date),
                MessageHandler(Filters.regex(
                    button('settings')), settings.display)
            ],
            "BOOKING_DATE": [
                MessageHandler(FilterDateTimeButtons(
                    date=True), booking.save_date),
                MessageHandler(Filters.regex(
                    button('back')), main_menu.display)
            ],
            "BOOKING_TIME": [
                MessageHandler(FilterDateTimeButtons(
                    time=True), booking.save_time),
                MessageHandler(Filters.regex(
                    button('back')), booking.get_date)
            ],
            "BOOKING_GET_COMMENTS": [
                MessageHandler(Filters.text, booking.save_comments),
                MessageHandler(Filters.regex(
                    button('back')), booking.get_time_slot)
            ],
            "BOOKING_REVIEW": [
                MessageHandler(Filters.regex(
                    button('submit')), booking.submit),
                MessageHandler(Filters.regex(button('cancel')), booking.cancel)
            ],
            "SETTINGS": [
                MessageHandler(Filters.regex(
                    button('my_info')), settings.my_info),
                MessageHandler(Filters.regex(
                    button('change_info')), settings.change_info),
                MessageHandler(Filters.regex(
                    button('back')), main_menu.display)
            ],
            "MY_INFO": [
                MessageHandler(Filters.regex(
                    button('back')), settings.display)
            ],
        },
        fallbacks=[

        ]
    )

    dispatcher.add_handler(main_conversation)
    dispatcher.add_handler(MessageHandler(
        ReplyToMessageFilter(Filters.user(constants.BOT_ID)), group.reply_to_user))

    updater.start_polling()
    updater.idle()
