import datetime
import logging
import os
import textwrap

import vk_api
from PIL import Image, ImageDraw, ImageFont, ImageChops
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug
from ..Utils.utils import uploadImg, downloadImg
from .QuotePlug_utils import models as utils
from os import path


class QuoteGen(BasePlug):
    description = "Делает цитаты. Отвечаете на сообщение словом командой," \
                  " или пересылаете множество сообщений и опять также отвечаете"

    def set_wallpaper(self, user_id, path):
        user: utils.User = utils.User.get(utils.User.id == user_id)
        user.bg_file_name = path
        user.save()

    def get_wallpaper(self, user_id):
        with self.db_handler.db.atomic():
            if utils.User.get_or_none(id=user_id) == None:
                utils.User.create(id=user_id,
                                  bg_file_name=path.join(self.bot.get_resource_folder(), self.name, "background.jpg"))
        user: utils.User = utils.User.get(utils.User.id == user_id)
        return user.bg_file_name

    def __init__(self, bot):
        super(self.__class__, self).__init__(bot)
        self.res_dir = os.path.join(self.bot.get_resource_folder(), self.name)
        if not os.path.exists(self.res_dir):
            os.mkdir(self.res_dir)
        self.db_handler = utils.db_handler(os.path.join(self.res_dir, "database.db"))
        self.db_handler.db.connect()
        utils.User.create_table()

        @self.message_handler(keywords=['cit', 'цит', 'цитген', 'цитата'])
        def cit(_, peer_id, msg, event):
            text = ""
            author_id = 0
            if len(msg.split()) >= 2 and \
                    len(event.obj.message["attachments"]) > 0 and \
                    event.obj.message["attachments"][0]["type"] == "photo":
                path_file = path.join(self.bot.get_resource_folder(), self.name, f"background{event.obj.message['from_id']}.png")
                downloadImg(event.obj.message["attachments"][0]["photo"]["sizes"][-1]["url"], path_file)
                file = open(path_file, "r+")
                shit = Image.open(path_file)
                w, h = shit.size
                new_height = 720
                new_width = 1280
                shit: Image.Image = shit.resize((new_width, new_height), Image.ANTIALIAS)
                shit.save(path_file)

                self.set_wallpaper(event.obj.message["from_id"], path_file)

                return

            if len(event.obj.message["fwd_messages"]) > 0:
                author_id = event.obj.message["fwd_messages"][0]["from_id"]
                for message in event.obj.message["fwd_messages"]:
                    if message["from_id"] == author_id:
                        text += f'{message["text"]}\n'

            else:
                author_id = event.obj.message["reply_message"]["from_id"]
                text = event.obj.message["reply_message"]["text"]

            try:
                author_info = self.bot.vk.get_api().users.get(user_ids=author_id,
                                                          fields='photo_max')
            except vk_api.exceptions.ApiError:
                self.bot.send_message(peer_id, "Нельзя цитировать сообщество.")
                return
            first_name, last_name = author_info[0]["first_name"], author_info[0]["last_name"]
            avatar_url = author_info[0]["photo_max"]

            self.bot.send_message(peer_id, None, uploadImg(self, self.drawImage(self=self, author_id=author_id,
                                                                            author=f"{first_name} {last_name}",
                                                                            text=text,
                                                                            avatar_url=avatar_url)))

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
        from os import path
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
        use_bg_img: bool = False
        background = Image.open(self.get_wallpaper(author_id))

        img = Image.new("RGBA", (1280, 720), dark_scheme[0])
        draw = ImageDraw.Draw(img)
        theme = dark_scheme
        if theme is not light_scheme and not use_bg_img:
            draw.rectangle((0, 0, img.size), fill='rgb(0,0,0)')
            img.paste(background)

        font = ImageFont.truetype(path.join(self.bot.get_resource_folder(), self.name, "font.ttf"), size=30)
        watermark = Image.new("RGBA", img.size)
        waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")

        watermark_font = ImageFont.truetype(path.join(self.bot.get_resource_folder(), self.name, "font.ttf"), size=70)
        time = f'Время: {datetime.datetime.today().strftime("%H:%M:%S")}'
        date = f'Дата: {datetime.datetime.today().strftime("%Y-%m-%d")}'

        draw.text((300, 200), f"© {author}", fill=theme[1], font=font)
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
            draw.text((300, h), line, fill=theme[1], font=font)
            if len(line) > 60:
                h += height * 2
            else:
                h += height

        # Draw date & time
        draw.text((img.size[0] / 10, img.size[1] - font.size * 2), date, fill=theme[1], font=font)
        draw.text((img.size[0] / 10, img.size[1] - font.size * 3), time, fill=theme[1], font=font)
        #

        # Draw matermark
        waterdraw.text((img.size[0] / 10, img.size[1] / round(7)), "big mitya is watching you", font=watermark_font)
        watermask = watermark.convert("L").point(lambda x: min(x, 4))
        watermark.putalpha(watermask)
        #

        img.paste(avatar, (int(img.size[0] / 25), 200), avatar)
        img.paste(watermark, None, watermark)
        path: str = "cit.png"
        img.save(path)
        return path

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
