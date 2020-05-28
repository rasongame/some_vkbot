import json

import requests
from PIL import Image
from vk_api import bot_longpoll, VkUpload
from vk_api.utils import get_random_id

from ..bot import Bot


class ImagesFromAlbumPlug:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.name = "ImagesFromAlbum"
        self.description = "Send arts from some albums "
        self.version = "rolling"
        self.keywords = ('picrandom')
        self.whoCan = ''
        self.onStart()

    def __sendMessage(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def onStart(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        a = msg.split(" ")
        params = {

        }
        self.__sendMessage(peer_id, msg="brr")
        self.__sendMessage(peer_id, msg=f""" {self.bot.vk.method("photos.get", params)}""")
        return
