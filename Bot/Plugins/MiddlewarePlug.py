import logging

from vk_api import bot_longpoll
from os import path, mkdir
from Bot.Plugins import BasePlug
from random import choice


class MiddlewarePlug(BasePlug):
    keywords = []
    listen_all = True

    # middleware?
    def __init__(self, bot):
        super().__init__(bot)
        self.res_dir = path.join(self.bot.get_resource_folder(), self.name)
        if not path.exists(self.res_dir):
            mkdir(self.res_dir)

    def work(self, peer_id, msg: str, event: bot_longpoll.VkBotEvent):
        def send(name: str):
            if not path.exists(path.join(self.res_dir, f"{name}_quotes.txt")):
                return
            with open(path.join(self.res_dir, f"{name}_quotes.txt")) as f:
                user = self.bot.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
                line = choice(f.readlines())
                self.bot.send_message(peer_id, line.format(user['first_name']))

        if event.obj.action is not None:
            logging.info(f"{event.obj.action}")
            send(event.obj.action['type'])
