import vk_api


def print_raw(self, peer_id: int, msg: str, e):
    self.bot.vk.method("messages.send",
                       {"peer_id": peer_id, "message": e, "random_id": 0})
    return


def print_debug(self, peer_id: int, msg: str, event):
    try:
        args = msg.lower().split()[1]
    except IndexError:
        self.bot.send_message(peer_id, "Ты пропустил аргумент. Юзай /debug plugins or /debug raw")
        return
    if args == "plugins" or "плагины":
        print_plugins(self, peer_id, msg, event)
    elif args == "raw" or "raw":
        print_raw(self, peer_id, msg, event)


def print_json(self, peer_id: int, msg: str, event):
    self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": event, "random_id": 0})


def print_plugins(self, peer_id: int, msg: str, event):
    msg = "Загруженные плагины :: \n"
    for i, plug in enumerate(self.bot.plugins):
        d = '....'
        if i >= 10:
            d = ".."
        msg += f"{d}{i}: {plug.name}\n"
    self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": 0})
