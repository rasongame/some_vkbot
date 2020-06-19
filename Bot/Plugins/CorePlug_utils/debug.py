import vk_api
from ..BasePlug import BasePlug

def print_raw(self, peer_id: int, e: vk_api.bot_longpoll.VkBotEvent):

    self.bot.vk.method("messages.send",
                       {"peer_id": peer_id, "message": e, "random_id": 0})
    return


def print_plugins(self, peer_id: int):
    msg = "Загруженные плагины :: \n"
    for i, plug in enumerate(self.bot.plugins):
        msg += f"....{i}: {plug.name}\n"
    # print(d/ir(self))
    self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": 0})
