import logging
from datetime import timedelta

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class AnimeDetector(BasePlug):
    description = "Находит аниме по фото"
    version = "rolling"
    keywords = ('анименафото',)
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        """

        :param bot: Обьект бота

        """
        super(AnimeDetector, self).__init__(bot)


    def __send_message(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        try:
            image_url = event.object['attachments'][0]['photo']['sizes'][-1]['url']
            api = f'https://trace.moe/api/search'
            params = {
                'url': image_url
            }
            r = requests.get(api, params=params)
            encode = r.json()
            name = encode["docs"][0]["title_english"]
            episode = encode["docs"][0]["episode"]
            chance = round(encode['docs'][0]["similarity"] * 100)
            sec = round(encode["docs"][0]["from"])
            time = timedelta(seconds=sec)
            self.__send_message(peer_id, f"""Я думаю это: {name}
                       Серия: {episode}
                       Точность: {chance}%
                       Тайминг: {time}""")
        except IndexError:
            self.__send_message(peer_id, "Я хочу фото!")

