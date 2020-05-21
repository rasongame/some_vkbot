import logging

from vk_api.utils import get_random_id


class BasePlug:
    def __init__(self, bot: object):
        self.bot: object = bot
        self.name = "some name"
        self.description = "some description"
        self.version = "rolling"
        self.keywords = ('')
        self.whoCan = ''
        self.onStart()

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self) -> None:
        pass

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
