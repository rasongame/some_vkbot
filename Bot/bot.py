import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Any, Optional
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

    def __init__(self, group_id: int, token: str, config: dict):
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
        self.pool = ThreadPoolExecutor(
            int(config["bot"].get("threads") if config['bot'].get('threads') is not None else 2))
        self.futures = []
        self.version = "Rolling Version"
        self.event_handler = event_handler
        self.checkThread = checkThread
        self.db: dict = {}
        self.group_id = group_id
        self.__token__ = token
        self.__config__ = config
        self.is_debug = config['bot']['debug_mode']
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.__token__, api_version="5.131")
        self.__vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-2s %(asctime)s ]  %(message)-2s")

    def send_message(self, peer_id: int, msg: str, attachment=None) -> Optional[Any]:
        """
        :param peer_id:
        :param msg:
        :param attachment:
        :return:
        """
        return self.vk.method("messages.send",
                              {"disable_mentions": 1,
                               "peer_id": peer_id,
                               "message": msg,
                               "random_id": 0,
                               "attachment": attachment})

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
        if called_from not in ("group_event_handler", "message_new_event_handler"):
            logging.warning(f"requested access to VkClientToken from {called_from}")
        return self.__vk_client

    def get_config(self):
        called_from = inspect.stack()[1][3]
        if called_from not in ("group_event_handler", "message_new_event_handler"):
            logging.warning(f"requested access to config dict from {called_from}")
        return self.__config__

    def get_token(self):
        called_from = inspect.stack()[1][3]
        if called_from not in ("group_event_handler", "message_new_event_handler"):
            logging.warning(f"requested access to token from {called_from}")

        return self.__token__
