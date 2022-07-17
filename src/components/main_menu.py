from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from utils.text import text, button
import logging


def display(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    keyboard = [
        [button('book_session')],
        [button('my_info'), button('settings')]
    ]

    update.effective_message.reply_text(text('main_menu'),
                                        reply_markup=ReplyKeyboardMarkup(
                                            keyboard,
                                            resize_keyboard=True),
                                        parse_mode='HTML')
    logging.info("Main page for user_id %s with update_id %s",
                 user_id, update.update_id)

    return "MAIN_MENU"


def book_session(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    update.effective_message.reply_text("I am Nuriddin", parse_mode='HTML')

    return "BOOK_SESSION"


def my_info(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    update.effective_message.reply_text("I am Nuriddin", parse_mode='HTML')

    return "MY_INFO"


def settings(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    update.effective_message.reply_text("I am Nuriddin", parse_mode='HTML')

    return "SETTINGS"
