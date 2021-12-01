import logging
from typing import Iterable, List

import vk_api
from vk_api.bot_longpoll import VkBotEventType

from Bot.event_handler import PREFIXS


class BasePlug:
    version = "rolling"
    keywords = {}
    whoCan = ''
    listen_all = False
    is_basic = False

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

    def message_handler(self, keywords=None):
        def wrapper(callback):
            self.register_message_handler(callback, keywords=keywords)

        return wrapper

    def register_message_handler(self, func, keywords: [Iterable, str]):
        if isinstance(keywords, str):
            keywords = (keywords,)
        for keyword in keywords:
            self.keywords.update({keyword: func})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        cmd = self.get_cmd_from_msg(msg)
        if cmd in self.keywords.keys():
            self.keywords[cmd](self, peer_id=peer_id, msg=msg, event=event)
        return

    @staticmethod
    def get_cmd_from_msg(msg):
        cmd: str = ""
        has_prefix = msg.split()[0][0] in PREFIXS
        if has_prefix:
            cmd = msg.split()[0][1:]
        else:
            cmd = msg.split()[0]
        return cmd.lower()

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
