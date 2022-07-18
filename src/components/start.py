from telegram import ChatAction, Update
from telegram.ext import CallbackContext
from .register import register_user
from db.queries import create_table_if_not_exists, add_new_user, get_user
from src.constants import STATUS
from src.components import main_menu
from utils.text import text
from utils.filter import is_group
import logging
import time


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
    if is_group(user_id):
        return

    create_table_if_not_exists('users')

    # Fetch data from Database
    if len(get_user(user_id)) == 0:
        add_new_user(user_id)
        update.effective_message.reply_text(text('welcome'),
                                            parse_mode='HTML')
        context.bot.send_chat_action(user_id, action=ChatAction.TYPING)
        time.sleep(2)
        logging.info(
            'New user was added to the database, user_id: %s', user_id)

    db_user_data = get_user(user_id)
    user_status = db_user_data[0][-1]

    if user_status == STATUS[5]:
        update.effective_message.reply_text(
            text('welcome_back'), parse_mode='HTML')
        logging.info("Active user restarted the bot, user_id: %s", user_id)
        return main_menu.display(update, context)

    context.user_data.update(
        {
            "user_id": user_id,
            "current_status": user_status,
        }
    )

    return register_user(update, context)
