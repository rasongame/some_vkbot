import os

import requests
from PIL import Image
from vk_api import VkUpload
from .BasePlug import BasePlug


class CompressPlug(BasePlug):
    name = "Жмых"
    description = "Жмыхалка"

    def __init__(self, bot):
        super(CompressPlug, self).__init__(bot)
        res_dir = self.bot.get_resource_folder()
        if not os.path.exists(os.path.join(res_dir, 'CompressPlug')):
            os.mkdir(os.path.join(res_dir, 'CompressPlug'))

        self.path = os.path.join(res_dir, 'CompressPlug')

        @self.message_handler(keywords=['compress', 'жмых'])
        def compress(this, peer_id, msg: str, event):

            helps = """
                        Жмыхалка фоток, хорошо ломает психику неподготовленным личностям.
                        Жмыхает вашу прикрепленную фотку, так же
                        можно передавать степень жмыхнутости, пример:
                            /жмых 55 55
                            /жмых 59 80
                            /жмых 50

                            чем ниже значения, тем сильнее жмыханет
                            максимум для одного из знчений - 100
                            а дефолт - 40 40
                        """

            if len(event.obj["attachments"]) >= 1 \
                    and event.obj["attachments"][0]["type"] == "photo":
                url = event.obj["attachments"][0]["photo"]["sizes"][-1]["url"]

            elif event.obj.reply_message and len(event.obj.reply_message["attachments"]) >= 1 \
                    and event.obj.reply_message["attachments"][0]["type"] == "photo":
                url = event.obj["reply_message"]["attachments"][0]["photo"]["sizes"][-1]["url"]
            else:
                self.bot.send_message(peer_id, helps)
                return

            img_r = requests.get(url, stream=True)
            img_r.raw.decode_content = True
            img: Image = Image.open(img_r.raw)
            img.save(f"{self.path}/жмых.png", "PNG")
            # Скачали фоточку...
            # ------------------------
            #
            x, y = 50, 50
            args = msg.split(" ")
            print(len(args))
            if len(args) >= 3:
                try:
                    x = int(args[1])
                    y = int(args[2])
                except ValueError:
                    self.bot.send_message(peer_id, helps)
            elif len(args) == 2:
                try:
                    x = int(args[1])
                    y = int(args[1])
                except ValueError:
                    self.bot.send_message(peer_id, helps)

            if x > 100 or y > 100:
                self.bot.send_message(peer_id, helps)

            os.system(f"convert {self.path}/жмых.png -liquid-rescale {y}x{x}%\! {self.path}/жмых_бахнутый.png")
            os.remove(f"{self.path}/жмых.png")
            #
            # Загружаем фоточку в вк...
            # ------------------------
            upload = VkUpload(self.bot.vk)
            photo = upload.photo_messages(f"{self.path}/жмых_бахнутый.png")[0]
            self.bot.send_message(peer_id, " Ж М Ы Х ", f"photo{photo['owner_id']}_{photo['id']}")
            return
