import logging

import psycopg2
import vk_api
from psycopg2._psycopg import connection, cursor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from .Utils import db_wrapper


class Bot:
    def __init__(self, group_id: int, token: str, config: dict):
        self.db: dict = {}
        self.group_id = group_id
        self.token = token
        self.config = config
        self.version = "Rolling Version"
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token)
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        self.plugins = []
        self.disabledPlugins = []
        self.admins = []
        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-8s %(asctime)s ]  %(message)-2s")
    def _connect_to_bd(self):
        try:
            self.db["name"] = self.config["database"]["db_name"]
            self.db["server"] = self.config["database"]["server"]
            self.db["user"] = self.config["database"]["user"]
            self.db["password"] = self.config["database"]["password"]
            self.db["conn"]: connection = psycopg2.connect(dbname=self.db["name"], user=self.db["user"],
                                                           password=self.db["password"], host=self.db["server"])
            self.db["cursor"]: cursor = self.db["conn"].cursor()
            self.db["conn"].autocommit = True
            self.db["wrapper"]: db_wrapper.wrapper = db_wrapper.wrapper(self)
            logging.info(f"Successfully connected to DB")
        except (Exception, psycopg2.Error) as error:
            logging.error(f"Cant connect to DB: {error}")

    def run(self) -> None:
        self._connect_to_bd()
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                logging.info(f"{event.obj.from_id} in {event.obj.peer_id} sent: {event.obj.text}")
                for plug in self.plugins:
                    try:
                        if plug.hasKeyword(event.obj.text.split()[0]):
                            # logging.info("successfull work plugins")
                            plug.work(event.obj.peer_id, event.obj.text, event)
                    except IndexError:
                        pass
