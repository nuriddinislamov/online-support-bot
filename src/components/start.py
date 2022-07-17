from telegram import Update
from telegram.ext import CallbackContext
from utils.text import text
from db.queries import create_table_if_not_exists, add_new_user, get_user
from .register import register_user
from src.constants import STATUS
from src.components import main_menu
import logging


# ----------------------------------------------------------------
# Sample user_data JSON object
# {
#   user_id: Unique ID for the user
#   current_status: Status of the user
#   next_status: Next stage of user journey
# }
# ----------------------------------------------------------------


def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    create_table_if_not_exists('users')

    # Fetch data from Database
    db_user_data = get_user(user_id)

    context.user_data.update(
        {
            "user_id": user_id,
            "current_status": STATUS[1],
        }
    )

    if len(db_user_data) == 0:
        add_new_user(user_id)
        update.effective_message.reply_text(text('welcome'),
                                            parse_mode='HTML')
        logging.info(
            'New user was added to the database, user_id: %s', user_id)

    # May create a bug if the data is not submitted to the DB from context.user_data
    if get_user(user_id, 'status')[0] == STATUS[5]:
        update.effective_message.reply_text(
            text('welcome_back'), parse_mode='HTML')
        return main_menu.display(update, context)

    return register_user(update, context)
