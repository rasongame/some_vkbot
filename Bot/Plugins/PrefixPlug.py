import logging

import vk_api
from vk_api.utils import get_random_id
from .BasePlug import BasePlug
from ..Utils.db_wrapper import User

class PrefixPlug(BasePlug):
    event_type = ""
    def __init__(self, bot: object):
        self.bot: object = bot
        self.name = "PrefixPlug"
        self.description = "PrefixPlug"
        self.version = "rolling"
        self.keywords = ('префикс', 'prefix')
        self.whoCan = ''
        self.onStart()
    def prefix_cmd(self, event, msg):
        prefix = msg.split(" ", maxsplit=1)[1]
        result = self.bot.Users.create(user_id=int(event.obj.from_id),
                                       prefix=prefix,
                                       has_vip=False,
                                       has_admin=False, has_banned=False)
        result.save()

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        return 
        # self.prefix_cmd(event, msg)

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
