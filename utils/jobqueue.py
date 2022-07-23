from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from utils.text import text


def run_job(update: Update, context: CallbackContext, run_time=None):
    if run_time is None:
        raise Exception("Please specify time to run feedback job.")
    user_id = update.effective_chat.id

    context.job_queue.run_once(
        request_feedback, when=run_time, context=user_id, name=str(user_id))


def request_feedback(context: CallbackContext):
    job = context.job
    user_id = job.context

    keyboard = [[InlineKeyboardButton('⭐️' * i, callback_data=i)]
                for i in range(1, 6)]

    context.bot.send_message(user_id, text(
        'feedback_template'),
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML')

    context.bot.send_message(user_id, text(
        'ask_feedback'), reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')
