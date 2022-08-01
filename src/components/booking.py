from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from telegram.error import Unauthorized
from src.components import main_menu
from src.constants import GROUP_ID
from utils.text import button, text
from utils.build_markup import build_markup
from utils.datetime_slots import generate_date_slots, generate_time_slots
from utils.jobqueue import run_job
from db.queries import get_user
import logging
import datetime
import random
import pytz


def get_date(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    dates = generate_date_slots()
    keyboard = build_markup(dates, n_cols=2, footer_buttons=[button('back')])

    update.effective_message.reply_text(
        text('get_date'),
        reply_markup=ReplyKeyboardMarkup(keyboard,
                                         resize_keyboard=True),
        parse_mode='HTML')

    payload = {
        "session_id": update.update_id,
        "user_id": user_id
    }
    context.user_data.update(payload)

    logging.info("%s started submitting a booking, choosing date...", user_id)

    return "BOOKING_DATE"


def save_date(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    chosen_date = update.effective_message.text

    update.effective_message.reply_text(text('got_it'),
                                        parse_mode='HTML')

    payload = {
        "date": chosen_date
    }
    context.user_data.update(payload)

    logging.info("Date submitted and saved for user_id %s", user_id)

    return get_time_slot(update, context)


def get_time_slot(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    time_slots = generate_time_slots()

    keyboard = build_markup(time_slots, n_cols=3,
                            footer_buttons=[button('back')])

    update.effective_message.reply_text(
        text('get_time'),
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True), parse_mode='HTML'
    )

    return "BOOKING_TIME"


def save_time(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    chosen_time = update.effective_message.text

    update.effective_message.reply_text(text('got_it'),
                                        parse_mode='HTML')

    payload = {
        "time": chosen_time
    }
    context.user_data.update(payload)

    logging.info("Time submitted and saved for user_id %s", user_id)

    return get_comments(update, context)


def get_comments(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text('enter_comments'), parse_mode='HTML', reply_markup=ReplyKeyboardRemove())

    return "BOOKING_GET_COMMENTS"


def save_comments(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    comments = update.effective_message.text

    payload = {
        "comments": comments
    }
    context.user_data.update(payload)

    update.effective_message.reply_text(text('got_it'),
                                        parse_mode='HTML')

    logging.info("Comments submitted and saved for user_id %s", user_id)

    return review(update, context)


def review(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    db_user_data = get_user(user_id)[0]
    first_name = db_user_data[1]
    last_name = db_user_data[2]
    full_name = first_name + ' ' + last_name

    payload = {
        "user_id": user_id,
        "full_name": full_name,
        "phone_number": db_user_data[3],
        "level": db_user_data[4]
    }

    context.user_data.update(payload)

    data = context.user_data

    update.effective_message.reply_text(
        text('review_booking').format(
            data['date'],
            data['time'],
            data['comments'],
            full_name,
        ),
        reply_markup=ReplyKeyboardMarkup(
            [
                [button('submit')],
                [button('cancel')]
            ], resize_keyboard=True
        ),
        parse_mode='HTML')
    return "BOOKING_REVIEW"


def submit(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    user_data = context.user_data

    teacher_raw = get_user(user_id, 'teacher')[0][0]
    teacher = "null" if teacher_raw is None else teacher_raw

    msg = context.bot.send_message(GROUP_ID, text('group_message_template')
                                   .format(
        user_data['session_id'],
        user_id,
        user_data['full_name'],
        user_data['phone_number'],
        user_data['level'],
        user_data['date'] + ' ' + user_data['time'],
        teacher,
        user_data['comments']
    ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=button('approve'), callback_data='approve'),
             InlineKeyboardButton(text=button('deny'), callback_data='deny')]
        ]),
        parse_mode='HTML')

    context.bot_data.update({
        msg.message_id: user_id
    })

    # Tashkent timezone is UTC +5;
    without_timezone = datetime.datetime.strptime(
        user_data['date'], "%d-%m-%Y") + datetime.timedelta(
            # random time between 21.00 - 22.00 on a given date
            seconds=21*60*60 + random.randint(0, 3600)
    )

    timezone = pytz.timezone('Asia/Tashkent')

    final_time = timezone.localize(without_timezone)
    run_job(
        update, context,
        run_time=final_time)

    update.effective_message.reply_text(text('submitted'))

    return main_menu.display(update, context)


def cancel(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text('canceled'))

    return main_menu.display(update, context)


def handle_booking_approval(update: Update, context: CallbackContext):
    query = update.callback_query
    message = query.message

    if query.data == 'approve':
        status = '✅ Approved'

    if query.data == 'deny':
        status = '⛔️ Denied'

    message.edit_text(f"<b>{status}</b>\n" + message.text,
                      parse_mode='HTML',
                      entities=message.entities)
    # User ID text index
    uid_txt_idx = message.text.find("UID:")
    # Get the User ID from the text
    uid = message.text[uid_txt_idx + 5:].split('\n')[0]

    try:
        context.bot.send_message(uid, text('status_update').format(status),
                                 parse_mode='HTML')
    except Unauthorized:
        update.effective_message.reply_text(text('forbidden_reply'))
