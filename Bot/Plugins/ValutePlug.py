import logging

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class ValutePlug(BasePlug):
    name = "ValutePlug"
    description = "Рубль - доллар емае"
    keywords = ('курс',)

    def __init__(self, bot: object):
        super(self.__class__, self).__init__(bot)





    def __send_message(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        api = "https://www.cbr-xml-daily.ru/daily_json.js"
        r = requests.get(api)
        encode = r.json()
        usd = encode["Valute"]["USD"]["Value"]
        eur = encode["Valute"]["EUR"]["Value"]
        self.__send_message(peer_id, "Доллар: {}₽\nЕвро: {}₽".format(usd, eur))

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
