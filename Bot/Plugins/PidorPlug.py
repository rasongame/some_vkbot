from vk_api import bot_longpoll
from vk_api import exceptions
from vk_api.utils import get_random_id

from Bot.bot import Bot
from .BasePlug import BasePlug


class PidorPlug(BasePlug):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.name = "Pidor"
        self.version = "rolling"
        self.description = "Кто пидор, епта?"
        self.keywords = ('pidor',)

        self.onStart()

    def __sendMessage(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent):
        try:
            s = self.bot.vk.method("messages.getConversationMembers",
                                   {"peer_id": peer_id, "group_id": self.bot.group_id})
            self.__sendMessage(peer_id, s)
        except exceptions.ApiError as e:
            self.__sendMessage(peer_id, e)
        #

        return
