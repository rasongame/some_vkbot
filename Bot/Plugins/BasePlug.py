import logging
from typing import Iterable, List

import vk_api
from vk_api.bot_longpoll import VkBotEventType


class BasePlug:
    version = "rolling"
    keywords: List = []
    new_keywords = {}
    whoCan = ''
    listen_all = False

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

    def register_message_handler(self, func, keywords: [Iterable, str]):
        if isinstance(keywords, str):
            keywords = (keywords,)
        for keyword in keywords:
            self.new_keywords[keyword] = func
            self.keywords.append(keyword)

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        pass
    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
