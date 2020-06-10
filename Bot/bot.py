import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Union

import vk_api
import peewee
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent, VkBotEvent
from .Utils import db_wrapper, console
from datetime import datetime


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        logging.info(f"Затрачено времени: {datetime.now() - start}")
        return result

    return wrapper


class Bot:
    def __init__(self, group_id: int, token: str, config: dict):
        self.db: dict = {}
        self.group_id = group_id
        self.token = token
        self.config = config
        self.version = "Rolling Version"
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token)
        self.vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        self.plugins = []
        self.disabledPlugins = []
        self.admins = []
        self.pool = ThreadPoolExecutor(8)
        self.futures = []
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

    def eventHandler(self, event):


        if event.type == VkBotEventType.MESSAGE_NEW:
            user = {}
            try:
                user = self.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
            except vk_api.exceptions.ApiError:
                user["first_name"] = "bot"
                user["last_name"] = "bot"

            logging.info(f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
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

    def run(self) -> None:
        self._connect_to_bd()
        event: Union[VkBotEvent, VkBotMessageEvent]
        # for event in self.longpoll.listen():
        # self.eventHandler(event)
        [self.eventHandler(event) for event in self.longpoll.listen()]
        # Эта страшная хероборина в теории должна быть быстрей
        # Но я как-то не уверен
