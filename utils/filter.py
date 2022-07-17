from telegram.ext import MessageFilter
from utils.text import j, button


class FilterButton(MessageFilter):
    def __init__(self, key: str):
        self.key = key

    def filter(self, message):
        return button(self.key) in message.text


def multibuttons(key: str):
    options = j["buttons"][key]
    return '|'.join(i for i in options)
