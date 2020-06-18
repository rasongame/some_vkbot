import datetime
import logging
import textwrap

import vk_api
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug
from ..Utils.utils import uploadImg, downloadImg


class QuoteGen(BasePlug):
    name = "QuoteGen"
    description = "Делает цитаты. Отвечаете на сообщение словом командой," \
                  " или пересылаете множество сообщений и опять также отвечаете"
    version = "rolling"
    keywords = ('cit', "цитген", 'цит')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot

        self.onStart()

    @staticmethod
    def drawImage(self, author: str, text: str, avatar_url: str) -> str:
        """
        :param self: self
        :param author: автор цитаты
        :param text: текст цитаты
        :param avatar_url: ссылка на аватар
        :return: путь к файлу.
        """
        w = textwrap.TextWrapper(width=60)
        dark_scheme = (
            (0, 0, 0, 0), 'rgb(255,255,255)'
        )
        light_scheme = (
            (255, 255, 255, 255), 'rgb(128,128,128)'
        )
        img = Image.new("RGBA", (1920, 1080), dark_scheme[0])
        draw = ImageDraw.Draw(img)
        theme = dark_scheme
        if theme is not light_scheme:
            draw.rectangle((0, 0, img.size), fill='rgb(0,0,0)')
        font = ImageFont.truetype("font.ttf", size=45)
        watermark = Image.new("RGBA", img.size)
        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")

        watermark_font = ImageFont.truetype("font.ttf", size=120)
        time = datetime.datetime.today().strftime("Время: %H:%M:%S")
        date = datetime.datetime.today().strftime("Дата: %Y-%m-%d")

        draw.text((400, 400), f"{author} сказал: ", fill=theme[1], font=font)
        avatar = Image.open(downloadImg(avatar_url), 'r')
        h = 400 + font.size
        lines = w.wrap(text)
        for line in lines:
            width, height = font.getsize(line)
            draw.text((400, h), line, fill=theme[1], font=font)
            h += height

        draw.text((img.size[0] / 10, img.size[1] - font.size * 2), date, fill=theme[1], font=font)
        draw.text((img.size[0] / 10, img.size[1] - font.size * 3), time, fill=theme[1], font=font)
        waterdraw.text((img.size[0] / 10, img.size[1] / round(7)), "https://vk.com/club184995795", font=watermark_font)
        watermask = watermark.convert("L").point(lambda x: min(x, 4))
        watermark.putalpha(watermask)
        img.paste(avatar, (int(img.size[0] / 13), int(img.size[1] / 2) - 150))
        img.paste(watermark, None, watermark)
        path: str = "/tmp/cit.png"
        img.save(path)
        return path

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __sendMessage(self, peer_id: int, msg: str):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def __sendMessage_with_img(self, peer_id: int, msg: str, attachment: str) -> None:
        return self.bot.vk.method("messages.send",
                                  {"peer_id": peer_id, "message": msg, "random_id": get_random_id(),
                                   'attachment': attachment})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        text = ""
        author_id = 0
        logging.info(event.obj)
        if len(event.obj["fwd_messages"]) > 0:
            author_id = event.obj["fwd_messages"][0]["from_id"]
            for message in event.object.fwd_messages:
                text += f'{message["text"]}\n'

        else:
            author_id = event.obj["reply_message"]["from_id"]
            text = event.object.reply_message["text"]

        author_info = self.bot.vk.get_api().users.get(user_ids=author_id,
                                                      fields='photo_max')
        first_name, last_name = author_info[0]["first_name"], author_info[0]["last_name"]
        avatar_url = author_info[0]["photo_max"]

        # logging.info(author_name)
        self.__sendMessage_with_img(peer_id, None, uploadImg(self,
                                                             self.drawImage(f"{first_name} {last_name}",
                                                                            text,
                                                                            avatar_url)))

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
