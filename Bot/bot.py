import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import vk_api
import peewee
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent, VkBotEvent
from .Utils import db_wrapper, console
from datetime import datetime
from .bot_utils import eventHandler as eHandler

def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        logging.info(f"Затрачено времени: {datetime.now() - start}")
        return result

    return wrapper


class Bot:
    plugins = []
    disabledPlugins = []
    admins = []
    pool = ThreadPoolExecutor(8)
    futures = []
    version = "Rolling Version"
    eventHandler = eHandler
    def __init__(self, group_id: int, token: str, config: dict):
        self.db: dict = {}
        self.group_id = group_id
        self.token = token
        self.config = config
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token)
        self.vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)

        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-8s %(asctime)s ]  %(message)-2s")

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



    def run(self) -> None:
        self._connect_to_bd()
        event: Union[VkBotEvent, VkBotMessageEvent]
        # for event in self.longpoll.listen():
        # self.eventHandler(event)
        [self.eventHandler(event) for event in self.longpoll.listen()]
        # Эта страшная хероборина в теории должна быть быстрей
        # Но я как-то не уверен
