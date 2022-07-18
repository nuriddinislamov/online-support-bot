from telegram.ext import MessageFilter
from utils.text import j
from utils.datetime_slots import generate_date_slots, generate_time_slots


from typing import Dict, Optional, Union
from telegram import Update
from telegram.ext import BaseFilter, UpdateFilter


class ReplyToMessageFilter(UpdateFilter):
    """
    Applies filters to ``update.effective_message.reply_to_message``.
    Args:
        filters (:class:`telegram.ext.BaseFilter`): The filters to apply. Pass exactly like passing
            filters to :class:`telegram.ext.MessageHandler`.
    Attributes:
        filters (:class:`telegram.ext.BaseFilter`): The filters to apply.
    """

    def __init__(self, filters: BaseFilter):
        self.filters = filters
        self.data_filter = self.filters.data_filter

    def filter(self, update: Update) -> Optional[Union[bool, Dict]]:
        if not update.effective_message.reply_to_message:
            return False

        reply_to_message = update.effective_message.reply_to_message
        if update.channel_post:
            return self.filters(Update(1, channel_post=reply_to_message))
        if update.edited_channel_post:
            return self.filters(Update(1, edited_channel_post=reply_to_message))
        if update.message:
            return self.filters(Update(1, message=reply_to_message))
        if update.edited_message:
            return self.filters(Update(1, edited_message=reply_to_message))
        return False


class FilterDateTimeButtons(MessageFilter):
    def __init__(self, date=False, time=False):
        self.date = date
        self.time = time

    def filter(self, message):
        if self.date is False and self.time is False:
            raise Exception("Provide either date or time")
        elif self.date is True and self.time is True:
            raise Exception("Choose either date or time")
        else:
            if self.date:
                return message.text in generate_date_slots()
            if self.time:
                return message.text in generate_time_slots()


def multibuttons(key: str):
    options = j["buttons"][key]
    return '|'.join(f"^{i}$" for i in options)


def is_group(chat_id: int):
    return True if chat_id < 0 else False
