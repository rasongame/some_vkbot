import logging

import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id


class BasePlug:
    version = "rolling"
    keywords = ('',)
    whoCan = ''

    def __init__(self, bot):
        """

        :param bot:
        """
        self.bot = bot
        if not hasattr(self, "name"):
            self.name = self.__class__.__name__
        if not hasattr(self, "description"):
            self.description = f"A {self.__class__.__name__} plugin"
        if not hasattr(self, "version"):
            self.version = "rolling"

        self.on_start()

    def has_keyword(self, keyword: str) -> bool:
        """
        Возращает True, если кейворд есть в списке кейвордов
        :param keyword:
        :return:

        """
        return keyword in self.keywords

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        pass

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
