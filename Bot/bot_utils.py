import logging
from concurrent.futures import as_completed

import peewee

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
        db_wrapper.database.initialize(self.db["wrapper"])
        db_wrapper.Chats.create_table()
        self.db["Users"] = db_wrapper.Users
        self.db["Example"] = db_wrapper.Example
        self.db["Chats"] = db_wrapper.Chats
        logging.info(f"Successfully connected to DB with IP: {self.db['server']}")
    except Exception as e:
        logging.error(e)


