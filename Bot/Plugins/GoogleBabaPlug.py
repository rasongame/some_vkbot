import logging
import os
from time import time

import vk_api
from gtts import gTTS
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class GoogleBabaPlug(BasePlug):
    name = "Google Baba"
    description = "Озвучка от Google TTS"
    keywords = ('озвучь', 'скажи', 'say')

    def __init__(self, bot: object):
        super(GoogleBabaPlug, self).__init__(bot)

    def __send_message(self, peer_id, msg, file=""):
        try:
            upload = VkUpload(self.bot.vk)
            audio = upload.audio_message(file, peer_id=peer_id, group_id=self.bot.group_id)['audio_message']
        finally:
            os.remove(file)
        self.bot.send_message(peer_id, msg, attachment=f"audio_message{audio['owner_id']}_{audio['id']}")

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        name = f"tts-{peer_id}-{time()}"
        text = msg.split(maxsplit=1)[1]
        tts = gTTS(text, lang="ru")
        tts.save(f"{name}.mp3")
        self.__send_message(peer_id, "", f"{name}.mp3")

    def on_start(self) -> None:
        logging.info(f"{self.name} is loaded")

    def on_stop(self) -> None:
        logging.info(f"{self.name} is disabling")
