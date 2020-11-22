import logging

import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id


class BasePlug:
    name = "some name"
    description = "some description"
    version = "rolling"
    keywords = ('',)
    whoCan = ''

    def __init__(self, bot: object):
        """

        :param bot:
        """
        self.bot: object = bot
        self.onStart()

    def hasKeyword(self, keyword: str) -> bool:
        """
        Возращает True, если кейворд есть в списке кейвордов
        :param keyword:
        :return:

        """
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg):
        """

        :param peer_id:
        :param msg:
        :return:

        """
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        pass

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
