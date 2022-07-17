import os
import dotenv
import logging
from telegram.ext import (Updater,
                          CommandHandler,
                          ConversationHandler, MessageHandler, Filters)
from src.components import start, register, main_menu
from utils.db import check_db_exists
from utils.text import button


dotenv.load_dotenv()

# Set Debug to False when in production!
DEBUG = os.environ.get('DEBUG', True)


logging.basicConfig(
    filename='logs.log' if not DEBUG else None,
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
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
                MessageHandler(Filters.text, register.save_data)
            ],
            "REQUEST_PHONE": [
                MessageHandler(Filters.text | Filters.contact,
                               register.save_data)
            ],
            "REQUEST_LEVEL": [
                MessageHandler(Filters.text, register.save_data)
            ],
            "MAIN_MENU": [
                MessageHandler(Filters.regex(
                    button('my_info')), main_menu.my_info),
                MessageHandler(Filters.regex(
                    button('settings')), main_menu.settings),
                MessageHandler(Filters.regex(
                    button('book_session')), main_menu.book_session)
            ]
        },
        fallbacks=[

        ]
    )

    dispatcher.add_handler(main_conversation)

    updater.start_polling()
    updater.idle()
