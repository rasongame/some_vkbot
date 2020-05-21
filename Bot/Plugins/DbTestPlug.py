import logging

from vk_api.utils import get_random_id

from .BasePlug import BasePlug
from ..bot import Bot
import psycopg2, vk_api
from psycopg2._psycopg import connection, cursor
from Bot.bot import Bot

class DbTestPlug(BasePlug):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        self.name = "DbTest"
        self.description = "DB integration test"
        self.version = "rolling"
        self.keywords = ('db', 'дб')
        self.arguments = ('add', 'адд',
                          'delete', 'делете',
                          'list', 'лист')
        self.whoCan = self.bot.admins
        self.db_name = self.bot.config["database"]["db_name"]
        self.db_server = self.bot.config["database"]["server"]
        self.db_user = self.bot.config["database"]["user"]
        self.db_password = self.bot.config["database"]["password"]
        self.onStart()
    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def writeToTable(self, author_id: int, message):
        pass
    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        if event.obj["from_id"] not in self.whoCan:
            logging.warning("Permission denied")
            return

        splitted = msg.split(" ")
        argument = splitted[1]
        toIns = splitted[2]
        if argument in self.arguments[0:1]:
            query = """ INSERT INTO example (author_id, message) VALUES(%s, %s)"""
            record = (peer_id, toIns)
            self.cursor.execute(query, record)
            self.conn.commit()
            self.__sendMessage(peer_id, "Inserted successfully")
        # if argument in self.arguments[3:4]:
        #     pass
        elif argument in self.arguments[4:5]: # list
            query = """SELECT * FROM example"""
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            print(records)

            toSend = "\n"
            for row in records:
                toSend += f"\nID; AUTHOR_ID; MESSAGE;"
                toSend += f"\n{row[0]}\t{row[1]}\t{row[2]}\t"

            self.__sendMessage(peer_id, toSend)
        return

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")


        try:
            self.conn: connection = psycopg2.connect(dbname=self.db_name, user=self.db_user,
                                                 password=self.db_password, host=self.db_server)
            self.cursor: cursor = self.conn.cursor()
            # postgres_insert_query = """ INSERT INTO example (author_id, message) VALUES (%s,%s)"""
            # record_to_insert = (, "sdas")
            # self.cursor.execute(postgres_insert_query, record_to_insert)
            # self.conn.commit()
        except (Exception, psycopg2.Error) as error:
            logging.error(f"{self.name}: {error}")


        finally:
            logging.info(f"{self.name} is writing to table")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
