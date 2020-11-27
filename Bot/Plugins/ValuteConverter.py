import logging

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class ValuteConverter(BasePlug):
    name = "ValuteConverter"
    description = "Конвертирует валюты"
    version = "rolling"
    keywords = ('конвертер', 'converter')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()




    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        api = "https://www.cbr-xml-daily.ru/daily_json.js"
        r = requests.get(api)
        encode = r.json()
        text = msg.split()
        usd = encode["Valute"]["USD"]["Value"]
        eur = encode["Valute"]["EUR"]["Value"]
        try:
            val = float(text[1])
        except ValueError:
            self.__sendMessage(peer_id, "Ты должен ввести цифру!\nНапример: /конвертер 5 usd")
        if val <= 0:
            self.__sendMessage(peer_id, "Число должно быть больше 0!")
        elif text[2] == "usd":
            self.__sendMessage(peer_id,
                               f"💰{'%g' % val}$:\nВ рублях: {round(val * usd, 3)}₽\nВ евро: {round(val * usd / eur, 3)}€")
        elif text[2] == "eur":
            self.__sendMessage(peer_id,
                               f"💰{'%g' % val}€:\nВ рублях: {round(val * eur, 3)}₽\nВ долларах:{round(val * eur / usd, 3)}$")
        else:
            self.__sendMessage(peer_id, "Выбери: usd или eur!\nНапример: /конвертер 5 usd")

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
