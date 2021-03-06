from re import match

from aiotg import Chat

from plugins import Intent


class Echo(Intent):

    @property
    def command(self) -> str:
        return r'/echo (.+)'

    async def execute(self, chat: Chat, rematch: match):
        chat.reply(rematch.group(1))
