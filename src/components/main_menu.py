from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from src.constants import ADMIN_IDS
from src.components import main_menu
from utils.text import text, button
from db.constants import DB_NAME
import logging
import pandas
import datetime
import sqlite3
import os


def display(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    keyboard = [
        [button('book_session')],
        [button('settings')]
    ]

    update.effective_message.reply_text(
        text('main_menu'),
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True),
        parse_mode='HTML')
    logging.info("Main page for user_id %s with update_id %s",
                 user_id, update.update_id)

    return "MAIN_MENU"


# Admin restricted only

def download_users(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    if user_id not in ADMIN_IDS:
        return main_menu.display(update, context)

    conn = sqlite3.connect(DB_NAME, check_same_thread=False)

    if not os.path.exists('exports'):
        os.makedirs('exports')

    db_df = pandas.read_sql_query("SELECT * FROM users", conn)

    db_df.to_excel(f'exports/export_{datetime.date.today()}.xlsx')

    context.bot.send_document(chat_id=user_id,
                              document=open(f'exports/export_{datetime.date.today()}.xlsx', 'rb'))
