import logging

import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotEventType

class BasePlug:
    name = "some name"
    description = "some description"
    version = "rolling"
    keywords = ('',)
    whoCan = ''
    event_type = ""
    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        pass

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
