import gc
import math
import os

import psutil
import vk_api
from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class CorePlug(BasePlug):
    name = "Core Plug"
    version = "rolling"
    description = "Корневой плагин бота"
    keywords = ('хелп', 'help', 'инфо', 'info', 'raw', 'lmao', 'report', 'репорт', "жив?", "пинг", "ping")
    event_type = ""

    def __init__(self, bot):
        self.bot: object = bot

        self.onStart()

    def __sendMessage(self, peer_id: int, msg: object) -> object:
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def __raw(self, peer_id: int, e: vk_api.bot_longpoll.VkBotEvent):
        self.__sendMessage(peer_id=peer_id, msg=e)

    def __info(self, peer_id: int):
        stats = gc.get_stats()
        prepared_msg = f"""
                Привет, я Меттатон версии {self.bot.version}
                Памяти сьела: {convert_size(psutil.Process(os.getpid()).memory_info().rss)}
                Чтобы узнать что я умею - введи /help или !хелп (можешь вводить с ! или / команды)
                Загруженные плагины ::
                """
        plug: BasePlug
        for i, plug in enumerate(self.bot.plugins):
            prepared_msg += f"....{i}: {plug.name}\n"

        # {self.bot.plugins}
        self.__sendMessage(peer_id=peer_id, msg=prepared_msg)
        del prepared_msg
        return

    def __help(self, peer_id: int):
        plug_slice_cmds = ""
        for plug in self.bot.plugins:
            plug_slice_cmds += f"{plug.name} -> {', '.join(plug.keywords)} \n {plug.description} \n"
        # [ for plug in self.bot.plugins]
        prepared_msg = f"Список команд:\n" \
                       f"{plug_slice_cmds}"
        self.__sendMessage(peer_id=peer_id, msg=prepared_msg)
        del prepared_msg
        return

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent):
        print("wtf?/")
        cmd = msg.split()[0].lower()
        if cmd in self.keywords[:2]:  # говно ебучее, ищет команду в 1 и 2 элементе тупла
            self.__help(peer_id)
            return
        elif cmd in self.keywords[2:4]:
            self.__info(peer_id)
            return
        elif cmd in self.keywords[4]:
            self.__raw(peer_id, event)
            return
        elif cmd in self.keywords[5]:
            self.__sendMessage(peer_id, "максбот круто")

        elif cmd in self.keywords[6:8]:
            text = f"Репорт из чата {peer_id}: {event.obj.from_id} репортнул: {msg}"
            for admin_id in self.bot.admins:
                self.__sendMessage(admin_id, text)
        elif cmd in self.keywords[8:11]:
            self.__sendMessage(peer_id, "жив, цел, орёл!")
        else:
            pass
        return
