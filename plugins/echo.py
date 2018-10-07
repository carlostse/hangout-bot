from re import match
from aiotg import Chat
from plugins import Intent


class Echo(Intent):

    @property
    def command(self) -> str:
        return r'/echo (.+)'

    def execute(self, chat: Chat, rematch: match):
        return chat.reply(rematch.group(1))
