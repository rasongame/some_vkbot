import logging

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class ValutePlug(BasePlug):
    name = "ValutePlug"
    description = "Рубль - доллар емае"
    version = "rolling"
    keywords = ('курс',)
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        api = "https://www.cbr-xml-daily.ru/daily_json.js"
        r = requests.get(api)
        encode = r.json()
        usd = encode["Valute"]["USD"]["Value"]
        eur = encode["Valute"]["EUR"]["Value"]
        self.__sendMessage(peer_id, "Доллар: {}₽\nЕвро: {}₽".format(usd, eur))

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
