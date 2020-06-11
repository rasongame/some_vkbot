from time import sleep

from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from .BasePlug import BasePlug
from ..bot import Bot


class KillerPlug(BasePlug):
    name = "Killer"
    description = "Just killer. Not working btw"
    version = "rolling"
    keywords = ('destroy',)
    whoCan = ''
    event_type = ""
    def __init__(self, bot):
        self.bot: Bot = bot
        self.onStart()

    def _sendMessage(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def onStart(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        if event.obj.from_id in self.bot.admins:
            self._sendMessage(peer_id, "1")
            sleep(1)
            self._sendMessage(peer_id, "2")
            sleep(1)
            self._sendMessage(peer_id, "3")
            sleep(1)
            self._sendMessage(peer_id, "Звездочка гори! Бах нахуй, я сдох!")
            exit(0)
