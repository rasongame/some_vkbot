import logging
from datetime import timedelta

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType
from Bot.Plugins.BasePlug import BasePlug


class AnimeDetector(BasePlug):
    description = "Находит аниме по фото"
    def __init__(self, bot: object):
        """

        :param bot: Обьект бота

        """
        super(AnimeDetector, self).__init__(bot)

        @self.message_handler(keywords='анименафото')
        def find(this, peer_id, msg: str, event):

            try:
                image_url = event.object['attachments'][0]['photo']['sizes'][-1]['url']
            except IndexError:
                self.bot.send_message(peer_id, "Я хочу фото!")
                return
            
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
            self.bot.send_message(peer_id, f"""Я думаю это: {name}
                       Серия: {episode}
                       Точность: {chance}%
                       Тайминг: {time}""")
