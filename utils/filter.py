from telegram.ext import MessageFilter
from utils.text import j


class FilterButton(MessageFilter):
    def __init__(self, key: str):
        self.key = key

    def filter(self, message):
        return 'python-telegram-bot is awesome' in message.text


def buttons(key: str):
    options = j["buttons"][key]
    res = []
    for i in options:
        res.append(options[i])
    return '|'.join(j for j in res)
