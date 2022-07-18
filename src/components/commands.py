from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardMarkup
from utils.text import button, text


def help(update: Update, context: CallbackContext):
    """
    Send a friendly message to help to navigate the user in the bot
    """
    update.effective_message.reply_text(text('help'),
                                        reply_markup=ReplyKeyboardMarkup(
                                            [[button('thanks')]],
                                            resize_keyboard=True), parse_mode='HTML')
    return "HELP_INFO"


def contact(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        text('contact_details'), parse_mode='HTML')
