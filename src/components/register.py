from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from src.components import main_menu
from src.constants import STATUS
from utils.text import text, button
from utils.build_markup import build_markup
from db.queries import get_user, set_user, reset_user
import logging


def register_user(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user_status = context.user_data['current_status']

    if user_status == STATUS[0]:
        update.effective_message.reply_text(
            text('begin_registration'), parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
        return request_name(update, context)

    # If the registration was left incomplete,
    # then set user status to 'new_user' and # start again

    reset_user(user_id)

    context.user_data['current_status'] = STATUS[0]

    update.effective_message.reply_text(
        text('incomplete_registration'), parse_mode='HTML')
    return register_user(update, context)


def request_name(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    update.effective_message.reply_text(
        text('request_name'),
        parse_mode='HTML')
    logging.info("Name input request for %s", user_id)
    return "REQUEST_NAME"


def get_name(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    msg = update.effective_message.text.split(' ')

    if len(msg) != 2:
        update.effective_message.reply_text(
            text('name_error'), parse_mode='HTML')
        return request_name(update, context)

    set_user(user_id, {'first_name': msg[0].capitalize(),
             'last_name': msg[1].capitalize(), 'status': STATUS[2]})

    return request_phone(update, context)


def request_phone(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text('request_phone'),
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(button('send_phone_number'),
                                request_contact=True)]
            ], resize_keyboard=True
        ),
        parse_mode='HTML')

    return "REQUEST_PHONE"


def get_phone(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    message = update.effective_message

    if message.contact:
        phone_number = "+" + str(message.contact.phone_number)
    else:
        if update.message.text[:1] != '+':
            context.bot.send_message(user_id,
                                     text("invalid_phone"),
                                     parse_mode='HTML')
            return request_phone(update, context)
        try:
            int(update.message.text[1:])
        except ValueError:
            context.bot.send_message(user_id,
                                     text('phone_int_error'),
                                     parse_mode='HTML')
            return request_phone(update, context)
        phone_number = ''.join(update.message.text.split(' '))

    set_user(user_id, {'phone_number': phone_number, 'status': STATUS[3]})
    logging.info(
        "Phone number entered to the database for user_id: %s", user_id)

    return request_level(update, context)


def request_level(update: Update, context: CallbackContext):
    keyboard = build_markup(button('levels'), n_cols=1)

    update.effective_message.reply_text(
        text('request_level'), reply_markup=ReplyKeyboardMarkup(keyboard), parse_mode='HTML')

    return "REQUEST_LEVEL"


def get_level(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    message = update.effective_message.text

    set_user(user_id, {'level': message, 'status': STATUS[4]})

    return request_teacher(update, context)


def request_teacher(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text('request_teacher'), reply_markup=ReplyKeyboardRemove(), parse_mode='HTML')

    return "REQUEST_TEACHER"


def get_teacher(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    message = update.effective_message.text

    set_user(user_id, {'teacher': message})

    return registration_complete(update, context)


def registration_complete(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    set_user(user_id, {'status': STATUS[1]})

    first_name = get_user(user_id, 'first_name')[0][0]
    last_name = get_user(user_id, 'last_name')[0][0]

    print(first_name, last_name)

    full_name = first_name + ' ' + last_name

    update.effective_message.reply_text(
        text('registration_complete').format(full_name), parse_mode='HTML')

    return main_menu.display(update, context)
