from concurrent.futures._base import as_completed

from vk_api.bot_longpoll import VkBotEventType, VkBotMessageEvent
import logging
import vk_api
import peewee
from .Utils import db_wrapper
from concurrent.futures import as_completed
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

        self.db["wrapper"].connect()
        self.Users = db_wrapper.User(self.db["wrapper"])

        logging.info(f"Successfully connected to DB")
    except Exception as e:
        logging.error(e)


def eventHandler(self, event: VkBotMessageEvent):
    if event.type == VkBotEventType.MESSAGE_NEW:
        user = {}
        try:
            user = self.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
        except vk_api.exceptions.ApiError:
            user["first_name"] = "bot"
            user["last_name"] = "bot"
        for plug in self.plugins:
            try:
                if plug.hasKeyword(event.obj.text.lower().split()[0]):
                    # logging.info("successfull work plugins")
                    logging.info("Поток открылся")
                    if self.config['bot']["debug_mode"] == True:
                        plug.work(event.obj.peer_id, event.obj.text, event)
                    else:
                        self.futures.append(self.pool.submit(plug.work, event.obj.peer_id, event.obj.text, event))
                        self.pool.submit(self.checkThread)
            except IndexError:
                pass
        
        logging.info(f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
