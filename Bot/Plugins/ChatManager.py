from time import sleep

from vk_api import bot_longpoll
from vk_api.utils import get_random_id
import logging
from .BasePlug import BasePlug
from ..bot import Bot


class ChatManager(BasePlug):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.name = "ChatManager"
        self.description = "Manage your chat, blya"
        self.version = "rolling"
        self.keywords = ('getPrefix', 'setPrefix')
        self.whoCan = ''
        self.onStart()

    def _sendMessage(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def onStart(self):
        pass

    def register(self, peer_id):
        self.bot.db["wrapper"].register(peer_id)

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        cmd = msg.split(" ")[0]
        if cmd in self.keywords[0]:
            # logging.info("wtf")
            self._sendMessage(peer_id, self.bot.db["wrapper"].returnPrefix(event.obj.from_id))
        if cmd in self.keywords[1]:
            prefix = event.obj.text.split(" ", maxsplit=1)[1]
            self._sendMessage(peer_id, self.bot.db["wrapper"].setPrefix(event.obj.from_id, prefix))
        if event.obj.from_id not in self.bot.admins:
            return
