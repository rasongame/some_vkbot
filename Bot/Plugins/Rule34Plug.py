import logging
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
    version = "rolling"
    keywords = ('rule34', 'руле34')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg, attachment=""):
        self.bot.vk.method(
            "messages.send",
            {
                "peer_id": peer_id,
                "attachment": attachment,
                "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        url = "https://r34-json-api.herokuapp.com/posts"
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
            self.__sendMessage(peer_id, "вотъ", attachment=f"photo{photo['owner_id']}_{photo['id']},")
        except Exception as e:
            self.__sendMessage(peer_id, f"Ашыпка. {e}")

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
