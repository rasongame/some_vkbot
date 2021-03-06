from time import sleep

from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class KillerPlug(BasePlug):
    name = "Killer"
    description = "Just killer. Not working btw if running with(out?) debug mode"
    keywords = ('destroy',)

    def __init__(self, bot):
        super(KillerPlug, self).__init__(bot)

    def on_start(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        if event.obj.from_id in self.bot.admins:
            self.bot.send_message(peer_id, "1")
            sleep(1)
            self.bot.send_message(peer_id, "2")
            sleep(1)
            self.bot.send_message(peer_id, "3")
            sleep(1)
            self.bot.send_message(peer_id, "Звездочка гори! Бах нахуй, я сдох!")
            exit(0)
