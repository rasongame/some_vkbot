import logging

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class ValuteConverter(BasePlug):
    name = "ValuteConverter"
    description = "Конвертирует валюты"
    keywords = ('конвертер', 'converter')

    def __init__(self, bot: object):
        super(self.__class__, self).__init__(bot)

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
            self.bot.send_message(peer_id, "Ты должен ввести цифру!\nНапример: /конвертер 5 usd")
        if val <= 0:
            self.bot.send_message(peer_id, "Число должно быть больше 0!")
        elif text[2] == "usd":
            self.bot.send_message(peer_id,
                               f"💰{'%g' % val}$:\nВ рублях: {round(val * usd, 3)}₽\nВ евро: {round(val * usd / eur, 3)}€")
        elif text[2] == "eur":
            self.bot.send_message(peer_id,
                               f"💰{'%g' % val}€:\nВ рублях: {round(val * eur, 3)}₽\nВ долларах:{round(val * eur / usd, 3)}$")
        else:
            self.bot.send_message(peer_id, "Выбери: usd или eur!\nНапример: /конвертер 5 usd")

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
