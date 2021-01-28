import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List
from os import path
import os
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
import inspect
from .Plugins.BasePlug import BasePlug
from .bot_utils import checkThread
from .event_handler import event_handler


def timeit(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        logging.info(f"Затрачено времени: {datetime.now() - start}")
        return result

    return wrapper


class Bot:

    def __init__(self, group_id: int, token: str, config: dict) -> object:
        """

        :param group_id: ID группы
        :param token: Токен группы
        :param config: Словарь - конфиг
        Здесь выполняется инициализация всякой херни

        """

        self.resource_folder = config["bot"].get("resource_folder") or path.join(path.curdir, "resources")
        self.plugins: List[BasePlug] = []
        self.disabledPlugins: List[BasePlug] = []
        self.admins: List[int] = []
        self.pool = ThreadPoolExecutor(int(config["bot"].get("threads")) or 2)
        self.futures = []
        self.version = "Rolling Version"
        self.event_handler = event_handler
        # self._connect_to_bd = _connect_to_bd
        self.checkThread = checkThread
        self.db: dict = {}
        self.group_id = group_id
        self.__token = token
        self.__config = config
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.__token, api_version="5.110")
        self.__vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-2s %(asctime)s ]  %(message)-2s")

    def run(self) -> None:
        """
        Запускает бота
        :return:

        """
        [self.event_handler(self, event) for event in self.longpoll.listen()]

        # Эта страшная хероборина в теории должна быть быстрей
        # Но я как-то не уверен
    def get_resource_folder(self) -> str:
        if not path.exists(path.join(path.curdir, self.resource_folder)):
            os.mkdir(path.join(path.curdir, self.resource_folder))

        return self.resource_folder

    def get_vk_client(self):
        called_from = inspect.stack()[1][3]
        if called_from != "event_handler":
            logging.warning(f"requested access to VkClientToken from {called_from}")
        return self.__vk_client

    def get_config(self):
        called_from = inspect.stack()[1][3]
        if called_from != "event_handler":
            logging.warning(f"requested access to config dict from {called_from}")
        return self.__config

    def get_token(self):
        called_from = inspect.stack()[1][3]
        if called_from != "event_handler":
            logging.warning(f"requested access to token from {called_from}")

        return self.__token

