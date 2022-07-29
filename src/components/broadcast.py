from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import Unauthorized, BadRequest
from src.constants import ADMIN_IDS
from src.components import main_menu
from db.queries import get_all_users
from utils.text import button
import time


def request(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    if user_id not in ADMIN_IDS:
        return main_menu.display(update, context)

    update.effective_message.reply_text(
        "<b>Hey admin!</b>\n\nSend me a post and I will broadcast it to all subscribers",
        reply_markup=ReplyKeyboardMarkup(
            [
                [button('cancel_broadcast')]
            ], resize_keyboard=True
        ),
        parse_mode='HTML')

    return "BROADCASTING"


def send_all(update: Update, context: CallbackContext):
    post = update.effective_message

    users = get_all_users()

    progress = update.effective_message.reply_text(
        f"📢 Broadcast started. Progress <b>0/{len(users)}</b>", parse_mode='HTML')

    sent = 0
    for user in users:
        if user[0] in ADMIN_IDS:
            continue
        try:
            post.copy(user[0])
            time.sleep(0.05)
            sent += 1
            progress.edit_text(
                f"📢 Broadcast started. Progress <b>{sent}/{len(users)}</b>", parse_mode='HTML')
        except Unauthorized:
            continue

    update.effective_message.reply_text(
        f"<b>📢 Broadcast finished. Delivered to {sent} users</b>", parse_mode='HTML')

    return main_menu.display(update, context)


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text("⚠️ Operation cancelled!")
    return main_menu.display(update, context)
