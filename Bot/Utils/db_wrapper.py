from psycopg2.extensions import quote_ident


class wrapper:
    def __init__(self, bot: object):
        self.bot: object = bot
        self.cursor = self.bot.db["cursor"]
        self.conn = self.bot.db["conn"]

    def insert(self, toIns: tuple):
        self.cursor.execute("INSERT INTO example (author_id, message) VALUES (%s, %s)", toIns)