import datetime
import logging
import os
import textwrap

import vk_api
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont, ImageChops
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug
from ..Utils.utils import uploadImg, downloadImg
from ..bot import Bot

class QuoteGen(BasePlug):
    name = "QuoteGen"
    description = "Делает цитаты. Отвечаете на сообщение словом командой," \
                  " или пересылаете множество сообщений и опять также отвечаете"
    version = "rolling"
    keywords = ('cit', "цитген", 'цит')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: Bot  = bot
        self.res_dir = os.path.join(self.bot.get_resource_folder(), self.name)
        if not os.path.exists(self.res_dir):
            os.mkdir(self.res_dir)

        self.onStart()
    @staticmethod
    def crop_to_circle(im):
        bigsize = (im.size[0] * 4, im.size[1] * 4)
        mask = Image.new('L', bigsize, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, im.split()[-1])
        im.putalpha(mask)

    @staticmethod
    def drawImage(self, author_id: int, author: str, text: str, avatar_url: str) -> str:
        # TODO: Добавить поддержку кастомных задних фонов. Заюзать Peewee, иначе зачем я его добавил?
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
        background: Image = None
        use_bg_img: bool = False
        if os.path.exists(os.path.join(self.res_dir, 'background.jpg')):
            background = Image.open(os.path.join(self.res_dir, 'background.jpg'), 'r')
            use_bg_img = True

        img = Image.new("RGBA", (1920, 1080), dark_scheme[0])
        draw = ImageDraw.Draw(img)
        theme = dark_scheme
        if theme is not light_scheme and not use_bg_img:
            draw.rectangle((0, 0, img.size), fill='rgb(0,0,0)')
        elif use_bg_img:
            img.paste(background)

        font = ImageFont.truetype("font.ttf", size=45)
        watermark = Image.new("RGBA", img.size)
        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")

        watermark_font = ImageFont.truetype("font.ttf", size=120)
        time = f'Время: {datetime.datetime.today().strftime("%H:%M:%S")}'
        date = f'Дата: {datetime.datetime.today().strftime("%Y-%m-%d")}'

        draw.text((400, 200), f"© {author}", fill=theme[1], font=font)
        save_to = os.path.join(self.res_dir, f'avatar_{author_id}.png')
        avatar = Image.open(downloadImg(avatar_url, save_to), 'r').convert("RGBA")
        self.crop_to_circle(avatar)
        avatar.convert("RGB")
        # avatar = ImageOps.expand(avatar, border=(3,3,3,3), fill="black")
        h = 250
        lines = w.wrap(text)

        for line in text.split("\n"):

            if len(line) > 60:
                line = w.fill(line)
            print(line)

            width, height = font.getsize(line)
            draw.text((400, h), line, fill=theme[1], font=font)
            if len(line) > 60:
                h += height * 2
            else:
                h += height

        # Draw date & time
        draw.text((img.size[0] / 10, img.size[1] - font.size * 2), date, fill=theme[1], font=font)
        draw.text((img.size[0] / 10, img.size[1] - font.size * 3), time, fill=theme[1], font=font)
        #


        # Draw matermark
        waterdraw.text((img.size[0] / 10, img.size[1] / round(7)), "https://vk.com/club184995795", font=watermark_font)
        watermask = watermark.convert("L").point(lambda x: min(x, 4))
        watermark.putalpha(watermask)
        #




        img.paste(avatar, (int(img.size[0] / 13), 200), avatar)
        img.paste(watermark, None, watermark)
        path: str = "cit.png"
        img.save(path)
        return path

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
                if message["from_id"] == author_id:
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
                                                             self.drawImage(self=self, author_id=author_id,
                                                                            author=f"{first_name} {last_name}",
                                                                            text=text,
                                                                            avatar_url=avatar_url)))

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
