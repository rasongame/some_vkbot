import logging
import os
import random

import requests
import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug
from Bot.Utils.plug_utils import downloadfile


class Rule34Plug(BasePlug):
    name = "Rule 34"
    description = "Rule 34"
    keywords = ('rule34', 'руле34')

    def __init__(self, bot: object):
        super(self.__class__, self).__init__(bot)

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        url = "https://r34-json-api.herokuapp.com/posts"
        if len(msg.split()) <= 1:
            self.__send_message(peer_id, "Ашыпка. Вы забыли теги")
            return

        params = {
            "tags": "+".join(msg.split()[1:]),
            "limit": 200
        }
        try:
            r = requests.get(url, params=params).json()
            r = random.choice(r)
            file_url = r['file_url']
            tags = ", ".join(r['tags'])
            file_name = downloadfile(file_url)
            upload = VkUpload(self.bot.vk)
            photo = upload.photo_messages(f"{file_name['name']}")[0]
            self.bot.send_message(peer_id, "вотъ", attachment=f"photo{photo['owner_id']}_{photo['id']},")
            os.remove(file_name["name"])
        except Exception as e:
            self.bot.send_message(peer_id, f"Ашыпка. {e}")

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
