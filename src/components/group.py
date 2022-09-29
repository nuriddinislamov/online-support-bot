from telegram.ext import CallbackContext
from telegram import Update
from telegram.error import Unauthorized
from utils.text import text


def reply_to_user(update: Update, context: CallbackContext):
    try:
        if update.message.reply_to_message:
            response = update.message.text
            reply_id = update.message.reply_to_message.message_id
            user_id = context.bot_data[reply_id]
            context.bot.send_message(chat_id=user_id,
                                     text=text('group_response')
                                     .format(
                                         response),
                                     parse_mode='HTML')
            update.effective_message.reply_text(text('message_sent'))

    except KeyError:
        update.effective_message.reply_text(text('try_later_messages'))
    except Unauthorized:
        update.effective_message.reply_text(text('forbidden_reply'))
    except AttributeError:
        return
