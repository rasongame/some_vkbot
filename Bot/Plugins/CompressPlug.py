#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

import requests
import vk_api
from PIL import Image
from vk_api import VkUpload
from vk_api.utils import get_random_id


class CompressPlug:
    def __init__(self, bot: object):
        self.bot: object = bot
        self.name = "ЖмыхPlug"
        self.description = "Жмыхалка"
        self.version = "rolling"
        self.keywords = ("жмых", )

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id, msg, attachment=None):
        self.bot.vk.method("messages.send", {
            "peer_id": peer_id,
            "message": msg,
            "random_id": get_random_id(),
            "attachment": attachment})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        helps = """
                Жмыхалка фоток, хорошо ломает психику неподготовленным личностям.
                Жмыхает вашу прикрепленную фотку, так же
                можно передавать степень жмыхнутости, пример:
                    /жмых 55 55
                    /жмых 59 80
                    чем ниже значения, тем сильнее жмыханет
                    максимум для одного из знчений - 100
                    а дефолт - 40 40
                """
        url = ""
        try:
            url = event.obj["attachments"][0]["photo"]["sizes"][-1]["url"]
        except IndexError:
            self.__sendMessage(peer_id, msg=helps)
            return
        img_r = requests.get(url, stream=True)
        img_r.raw.decode_content = True
        img: Image = Image.open(img_r.raw)
        img.save(f"жмых.png", "PNG")
        # Скачали фоточку...
        #------------------------
        #
        x, y = 50,50
        args = msg.split(" ")
        if len(args) >= 2:
            try:
                x = int(args[1])
                y = int(args[2])
            except ValueError:
                self.sendmsg(helps)

        if x > 100 or y > 100:
            self.sendmsg(helps)
        os.system(f"convert жмых.png -liquid-rescale {y}x{x}%\! жмых_бахнутый.png")
        os.remove("жмых.png")
        #
        # Загружаем фоточку в вк...
        #------------------------
        upload = VkUpload(self.bot.vk)
        photo = upload.photo_messages(f"жмых_бахнутый.png")[0]
        self.__sendMessage(peer_id, "Ема жмыхнуло", f"photo{photo['owner_id']}_{photo['id']}")
        logging.info(url)