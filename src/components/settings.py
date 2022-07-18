from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from db.queries import get_user
from utils.text import text, button


def display(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    update.effective_message.reply_text(text('settings'),
                                        reply_markup=ReplyKeyboardMarkup(
        [
            [button('my_info')],
            [button('change_info')],
            [button('back')]
        ], resize_keyboard=True
    ), parse_mode='HTML')

    return "SETTINGS"


def my_info(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    db_user_data = get_user(user_id)[0]

    first_name = db_user_data[1]
    last_name = db_user_data[2]
    phone_number = db_user_data[3]
    level = db_user_data[4]

    full_name = str(first_name) + " " + str(last_name)

    update.effective_message.reply_text(
        text('my_info')
        .format(
            full_name, phone_number, level),
        reply_markup=ReplyKeyboardMarkup(
            [
                [button('back')]
            ], resize_keyboard=True
        ),
        parse_mode='HTML')

    return "MY_INFO"


def change_info(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        "DEMO VERSIYA TEKST!\n\n<b>QO'SHIMCHA XIZMAT</b> SIFATIDA BU BO'LIMNI HAM ISHGA TUSHIRSA BO'LADI", parse_mode='HTML')
