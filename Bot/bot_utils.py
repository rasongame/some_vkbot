import logging
from concurrent.futures import as_completed

import peewee
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotMessageEvent

from .Utils import db_wrapper


def checkThread(self):
    """
    Скинуть название исключения в потоке, ежели  такое произойдет
    :rtype: none
    """
    for x in as_completed(self.futures):
        if x.exception() is not None:
            logging.error(x.exception())
            print(f"ошибОЧКА разраба: {x.exception()}")
        self.futures.remove(x)
        logging.info("Поток закрылся")


def _connect_to_bd(self):
    try:
        self.db["name"] = self.config["database"]["db_name"]
        self.db["server"] = self.config["database"]["server"]
        self.db["user"] = self.config["database"]["user"]
        self.db["password"] = self.config["database"]["password"]
        self.db["wrapper"] = peewee.PostgresqlDatabase(
            self.db["name"],
            user=self.db["user"],
            password=self.db["password"],
            host=self.db["server"])
        # self.db["wrapper"].connect()
        # self.db["Users"] = assign(self.db["wrapper"])
        db_wrapper.database.initialize(self.db["wrapper"])
        db_wrapper.Chats.create_table()
        self.db["Users"] = db_wrapper.Users
        self.db["Example"] = db_wrapper.Example
        self.db["Chats"] = db_wrapper.Chats
        logging.info(f"Successfully connected to DB with IP: {self.db['server']}")
    except Exception as e:
        logging.error(e)


prefixs = (
    '/',
    '!',
)


def event_handler(self, event: VkBotMessageEvent):
    """
    Здесь выполняется обработка эвентов. Nuff said
    :param self:
    :param event:
    :return:

    """
    if event.type == VkBotEventType.MESSAGE_NEW:
        user = {}
        try:
            user = self.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
        except vk_api.exceptions.ApiError:
            user["first_name"] = "bot"
            user["last_name"] = "bot"
        if event.obj.text.startswith(prefixs):
            for plug in self.plugins:
                try:
                    cmd = event.obj.text.lower()
                    cmd_without_slash = str(cmd[1   :]).split()[0]
                    if plug.hasKeyword(cmd_without_slash):
                        # logging.info("successfull work plugins")
                        logging.info("Поток открылся")
                        if self.config['bot']["debug_mode"]:
                            plug.work(peer_id=event.obj.peer_id, event=event, msg=event.obj.text[1:])
                        else:
                            self.futures.append(
                                self.pool.submit(plug.work, peer_id=event.obj.peer_id, event=event, msg=event.obj.text[1:]))
                            self.pool.submit(self.checkThread)
                except IndexError:
                    pass

        logging.info(
            f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
