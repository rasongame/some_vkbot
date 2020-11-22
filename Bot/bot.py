import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

from .Plugins.BasePlug import BasePlug
from .bot_utils import _connect_to_bd, checkThread
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
        self.plugins: List[BasePlug] = []
        self.disabledPlugins: List[BasePlug] = []
        self.admins: List[int] = []
        self.pool = ThreadPoolExecutor(8)
        self.futures = []
        self.version = "Rolling Version"
        self.event_handler = event_handler
        # self._connect_to_bd = _connect_to_bd
        self.checkThread = checkThread
        self.db: dict = {}
        self.group_id = group_id
        self.token = token
        self.config = config
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token, api_version="5.110")
        self.vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-2s %(asctime)s ]  %(message)-2s")

    def run(self) -> None:
        """
        Запускает бота
        :return:

        """
        # _connect_to_bd(self)
        # for event in self.longpoll.listen():
        # self.event_handler(event)
        [self.event_handler(self, event) for event in self.longpoll.listen()]

        # Эта страшная хероборина в теории должна быть быстрей
        # Но я как-то не уверен
