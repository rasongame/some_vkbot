import vk_api
from vk_api import bot_longpoll

from vk_api.utils import get_random_id
from .BasePlug import BasePlug
from ..bot import Bot


class CorePlug(BasePlug):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.name = "Core Plug"
        self.version = "rolling"
        self.description = "Core plugin of bot.."
        self.keywords = 'info'
        self.onStart()
    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg, event: vk_api.bot_longpoll.VkBotEvent):
        prepared_msg = f"""
        metrobot version :: {self.bot.version}
        loaded plugins ::
        """
        plug: BasePlug
        for i, plug in enumerate(self.bot.plugins):
            prepared_msg += f"{i}: {plug.name} {plug.version}\n"

        # {self.bot.plugins}
        self.__sendMessage(peer_id=peer_id, msg=prepared_msg)
