import json

import requests
from PIL import Image
from vk_api import bot_longpoll, VkUpload
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class KonachanPlug(BasePlug):
    name = "Konachan"
    description = "Присылает арты с konachan.net"
    version = "rolling"
    keywords = ('konachan', 'коначан')
    whoCan = ''
    event_type = ""

    def __init__(self, bot):
        super(KonachanPlug, self).__init__(bot)


    def __send_message(self, peer_id: int, msg: str):
        return self.bot.vk.method("messages.send",
                                  {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def __sendMessage_with_img(self, peer_id: int, msg: str, attachment) -> None:
        return self.bot.vk.method("messages.send",
                                  {"peer_id": peer_id, "message": msg, "random_id": get_random_id(),
                                   'attachment': attachment})

    def on_start(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent):
        limit = msg.split(maxsplit=1)[1]
        try:
            if limit is None or int(limit) <= 1:
                limit = 1
        except ValueError:
            self.__send_message(peer_id, "Самый умный?")
            return

        if event.object["from_id"] not in self.bot.admins and int(limit) >= 3:
            limit = 5

        r = requests.get(f"https://konachan.net/post.json?limit={limit}&tags=order%3Arandom")
        json_parsed = json.loads(r.text)
        attachments = []
        self.__send_message(peer_id, "Начинаю выкачку...")
        for i, jsonx in enumerate(json_parsed):
            img_r = requests.get(jsonx["file_url"], stream=True)
            img_r.raw.decode_content = True
            img: Image = Image.open(img_r.raw)
            img.save(f"/tmp/foo{i}.png", "PNG")
            # logging.info(msg)
            upload = VkUpload(self.bot.vk)
            photo = upload.photo_messages(f"/tmp/foo{i}.png")[0]
            attachments.append(f"photo{photo['owner_id']}_{photo['id']},")

        attachment_str = ""
        for attachment in attachments:
            attachment_str += attachment
        self.__sendMessage_with_img(peer_id=peer_id, msg=None, attachment=attachment_str)
        return
