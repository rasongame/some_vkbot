import json

import requests
from PIL import Image
from vk_api import bot_longpoll, VkUpload
from vk_api.utils import get_random_id
from ..bot import Bot
from ..Utils.plug_utils import photo_getWallPhoto


class ImagesFromAlbumPlug:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.name = "ImagesFromAlbum"
        self.description = "Send arts from some albums "
        self.version = "rolling"
        self.keywords = ('каты', "юри", "яой")
        self.whoCan = ''
        self.onStart()

    def Cats_cmd(self, text, peer_id: int):
        attachment = photo_getWallPhoto(self.bot, "-43228812")
        self.__sendMessage_with_img(peer_id, "brr?", attachment=attachment)

    def Yuri_Cmd(self, text, peer_id: int):
        attachment = photo_getWallPhoto(self.bot, "-63092480")
        self.__sendMessage_with_img(peer_id, "brr?", attachment=attachment)

    def Yaoi_Cmd(self, text, peer_id: int):
        attachment = photo_getWallPhoto(self.bot, "-113004231")
        self.__sendMessage_with_img(peer_id, "brr?", attachment=attachment)

    def __sendMessage_with_img(self, peer_id: int, msg: str, attachment: str = "") -> None:
        return self.bot.vk.method("messages.send",
                                  {"peer_id": peer_id, "message": msg, "random_id": get_random_id(),
                                   'attachment': attachment})

    def onStart(self):
        pass

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        if msg.split()[0] == "каты":
            self.Cats_cmd(msg, peer_id)
        elif msg.split()[0] == "юри":
            self.Yuri_Cmd(msg, peer_id)
        elif msg.split()[0] == "яой":
            self.Yaoi_Cmd(msg, peer_id)
        else:
            pass

        return
