import logging

import vk_api
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug
from ..Utils.db_wrapper import Example as Example_table


class DbTestPlug(BasePlug):
    name = "some name"
    description = "append - добавить" \
                  "remove - удалить"
    version = "rolling"
    keywords = ('db', 'push', 'пуш')
    whoCan = ''
    event_type = ""

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def __append(self, peer_id, text):
        Example: Example_table = self.bot.db["Example"]
        Note = Example.create(message=text, author_id=peer_id)
        Note.save()

    def __get_list(self, peer_id):
        Example: Example_table = self.bot.db["Example"]
        return Example.select().where(Example.author_id == peer_id)

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        splt = msg.split(maxsplit=3)
        if splt[0] == self.keywords[0]:
            if splt[1] == "append":
                self.__append(event.obj.from_id, splt[2])
                self.__sendMessage(peer_id, "вставил")
            elif splt[1] == "list":
                msg = "Твои записи в БД"
                limit = 1
                try:
                    limit = int(splt[2])
                except ValueError:
                    limit = 5

                length = len(self.__get_list(event.obj.from_id))
                for i in enumerate(self.__get_list(event.obj.from_id)[length - limit:length]):
                    msg += f"\n {i[0]}. {i[1].message}"

                msg += f"\nПоказаны последние {limit} позиций"
                self.__sendMessage(peer_id, msg)
            return
        elif splt[0] in self.keywords[1:3]:
            if event.obj["from_id"] not in self.bot.admins:
                self.__sendMessage(peer_id, "я запрещаю тебе это делать!")
                return
            for chat in self.bot.db["Chats"]:
                self.__sendMessage(chat.chat_id, f"{msg.split(maxsplit=1)[1]}")
            return

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
