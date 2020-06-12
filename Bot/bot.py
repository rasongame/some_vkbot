import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Union

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent, VkBotEvent
from datetime import datetime
from .bot_utils import _connect_to_bd, checkThread, eventHandler

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
    eventHandler = eventHandler
    _connect_to_bd = _connect_to_bd
    checkThread = checkThread
    def __init__(self, group_id: int, token: str, config: dict):
        self.db: dict = {}
        self.group_id = group_id
        self.token = token
        self.config = config
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token, api_version="5.110")
        self.vk_client = vk_api.VkApi(token=config["bot"]["client_token"]).get_api()
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)

        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-2s %(asctime)s ]  %(message)-2s")




    def run(self) -> None:
        self._connect_to_bd()
        event: Union[VkBotEvent, VkBotMessageEvent]
        # for event in self.longpoll.listen():
        # self.eventHandler(event)
        [self.eventHandler(event) for event in self.longpoll.listen()]
        # Эта страшная хероборина в теории должна быть быстрей
        # Но я как-то не уверен
