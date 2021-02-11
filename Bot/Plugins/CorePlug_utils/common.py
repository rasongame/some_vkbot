import gc
import math
import os

import psutil


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def print_info(self, peer_id: int, **kwargs):
    stats = gc.get_stats()
    prepared_msg = f"""
            Привет, я Меттатон версии {self.bot.version}
            Памяти сьела: {convert_size(psutil.Process(os.getpid()).memory_info().rss)}
            Чтобы узнать что я умею - введи /help или !хелп (можешь вводить с ! или / команды)

            """

    self.bot.send_message(peer_id, prepared_msg)
    del prepared_msg
    return


def print_live(self, peer_id, msg, **kwargs): self.bot.send_message(peer_id, "жив, цел, орёл!")


def send_report(self, peer_id, msg, **kwargs):
    text = f"Репорт из чата {peer_id}: {kwargs['event'].obj.from_id} репортнул: {msg}"
    for admin_id in self.bot.admins:
        self.bot.send_message(admin_id, text)

    self.bot.send_message(peer_id, "Ваш репорт отослан!")


def print_help(self, peer_id: int, msg: str, **kwargs):
    plug_slice_cmds = ""
    for plug in self.bot.plugins:
        plug_slice_cmds += f"{plug.name} -> {', '.join(plug.keywords)} \n {plug.description} \n"
    prepared_msg = f"Список команд:\n" \
                   f"{plug_slice_cmds}"
    self.bot.send_message(peer_id, prepared_msg)
    del prepared_msg
    return


def print_start_info(self, peer_id, **kwargs):
    msg = \
        """
    Привет, я Меттатон, введи "помощь", чтобы узнать информацию.
    """
    self.bot.send_message(peer_id, msg)
    del msg
