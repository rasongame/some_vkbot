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
    def __init__(self, bot):
        self.bot: object = bot
        self.name = "Core Plug"
        self.version = "rolling"
        self.description = "Core plugin of bot.."
        self.keywords = ('хелп', 'help', 'инфо', 'info', 'raw', 'максбот')
        self.onStart()

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def __raw(self, peer_id: int, e: vk_api.bot_longpoll.VkBotEvent):
        self.__sendMessage(peer_id=peer_id, msg=e)

    def __info(self, peer_id: int):
        stats = gc.get_stats()
        prepared_msg = f"""
                Untitled bot version :: {self.bot.version}
                Memory eated: {convert_size(psutil.Process(os.getpid()).memory_info().rss)}
                GC Info: 
                    Enabled: {gc.isenabled()}
                    Stats: Collected: {stats[0]["collected"]}
                loaded plugins ::
                """
        plug: BasePlug
        for i, plug in enumerate(self.bot.plugins):
            prepared_msg += f"{i}: {plug.name} {plug.version}\n"

        # {self.bot.plugins}
        self.__sendMessage(peer_id=peer_id, msg=prepared_msg)
        del prepared_msg
        return

    def __help(self, peer_id: int):
        plug_slice_cmds = ""
        for plug in self.bot.plugins:
            plug_slice_cmds += f"\n{plug.name}: {plug.keywords}"

        prepared_msg = f"Список команд:" \
                       f"{plug_slice_cmds}" \
                       f"\nКоманды 2.1, 2.2 требуют наличия привилегий." \
                       f"\nДля disable и enable необходим номер плагина из info"
        self.__sendMessage(peer_id=peer_id, msg=prepared_msg)
        del prepared_msg
        return

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent):

        cmd = msg.split()[0]
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
        else:
            pass

        return
