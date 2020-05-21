import json

import requests
from PIL import Image
from vk_api import bot_longpoll, VkUpload
from vk_api.utils import get_random_id

from ..bot import Bot


class KonachanPlug:
    def __init__(self, bot):
        self.bot: Bot = bot
        self.name = "Konachan"
        self.description = "Send arts from Konachan"
        self.version = "rolling"
        self.keywords = ('konachan')
        self.whoCan = ''
        self.onStart()

    def __sendMessage(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def onStart(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        r = requests.get("http://konachan.net/post.json?limit=1")
        json_parsed = json.loads(r.text)
        self.__sendMessage(peer_id=peer_id, msg=json_parsed[0]["file_url"])
        img_r = requests.get(json_parsed[0]["file_url"], stream=True)
        img_r.raw.decode_content = True
        img: Image = Image.open(img_r.raw)
        img.save("/tmp/foo.shit", "PNG")
        with open("/tmp/foo.shit") as file:
            upload = VkUpload(self.bot.vk)
            photo = upload.photo_messages(photos="/tmp/foo.shit")
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'
            self.__sendMessage(peer_id=peer_id, attachment=attachment)
        return
