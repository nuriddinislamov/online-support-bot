from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from db.queries import get_user
from src.constants import FEEDBACK_GROUP_ID
from src.components import main_menu
from utils.text import button, text


def handle_feedback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    context.user_data.update(
        {
            "feedback_stars": int(data)
        }
    )
    query.answer()
    update.effective_message.reply_text(text('stars_submitted')
                                        .format(int(data) * "⭐️"),
                                        parse_mode='HTML')
    query.delete_message()
    return request_comments(update, context)


def request_comments(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    skip = [
        [button('no_comments')]
    ]
    context.bot.send_message(user_id, text(
        'feedback_comments'),
        reply_markup=ReplyKeyboardMarkup(skip, resize_keyboard=True),
        parse_mode='HTML')

    return "FEEDBACK_COMMENTS"


def submit_feedback(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    first_name = get_user(user_id, 'first_name')[0][0]
    last_name = get_user(user_id, 'last_name')[0][0]
    level = get_user(user_id, 'level')[0][0]
    stars = context.user_data['feedback_stars'] * "⭐️"
    comments = update.effective_message.text

    context.bot.send_message(FEEDBACK_GROUP_ID,
                             text('feedback_to_group')
                             .format(
                                 update.update_id,
                                 user_id,
                                 first_name + ' ' + last_name,
                                 level,
                                 stars,
                                 comments
                             ), parse_mode='HTML')

    update.effective_message.reply_text(
        text('feedback_submitted'), parse_mode='HTML')

    return main_menu.display(update, context)
