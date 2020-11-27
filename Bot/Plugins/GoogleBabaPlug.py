import logging
import os
from datetime import datetime

import vk_api
from gtts import gTTS
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class GoogleBabaPlug(BasePlug):
    name = "Google Baba"
    description = "some description"
    version = "rolling"
    keywords = ('озвучь', 'скажи', 'say')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()


    def __sendMessage(self, peer_id, msg, file=""):
        try:
            upload = VkUpload(self.bot.vk)
            audio = upload.audio_message(file, peer_id=peer_id, group_id=self.bot.group_id)['audio_message']
        finally:
            os.remove(file)
        self.bot.vk.method("messages.send", {
            "peer_id": peer_id,
            "message": msg,
            "attachment": f"audio_message{audio['owner_id']}_{audio['id']}",
            "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        name = datetime.now()
        text = msg.split(maxsplit=1)[1]
        tts = gTTS(text, lang="ru")
        tts.save(f"{name}.mp3")
        self.__sendMessage(peer_id, "", f"{name}.mp3")

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
