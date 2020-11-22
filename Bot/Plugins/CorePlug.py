
import vk_api
from vk_api import bot_longpoll
from vk_api.utils import get_random_id
from .CorePlug_utils.debug import *
from .CorePlug_utils.common import *
from .BasePlug import BasePlug


class CorePlug(BasePlug):
    name = "Core Plug"
    version = "rolling"
    description = "Корневой плагин бота"
    keywords = ('хелп', 'help',
                'инфо', 'info',
                ' ', ' ',
                'report', 'репорт',
                "жив?", "пинг", "ping",
                "debug", "дебаг")
    event_type = ""
    def __init__(self, bot):
        self.bot: object = bot

        self.onStart()

    def __sendMessage(self, peer_id: int, msg: object):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})



    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent):
        print("wtf?/")
        cmd = msg.split()[0].lower()

        if cmd in self.keywords[:2]:  # говно ебучее, ищет команду в 1 и 2 элементе тупла
            print_help(self, peer_id, msg)
            return
        elif cmd in self.keywords[2:4]:
            print_info(self,peer_id)
            return
        elif cmd in self.keywords[6:8]:
            text = f"Репорт из чата {peer_id}: {event.obj.from_id} репортнул: {msg}"
            for admin_id in self.bot.admins:
                self.__sendMessage(admin_id, text)
        elif cmd in self.keywords[8:11]:
            self.__sendMessage(peer_id, "жив, цел, орёл!")
        elif cmd in self.keywords[11:13]:
            args = msg.lower().split()[1]
            if args == "plugins" or "плагины":
                print_plugins(self, peer_id)
            elif args == "raw" or "raw":
                print_raw(self, peer_id, event)


        return
