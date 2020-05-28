from psycopg2 import sql
from psycopg2.extensions import quote_ident


class wrapper:
    def __init__(self, bot: object):
        self.bot: object = bot
        self.cursor = self.bot.db["cursor"]
        self.conn = self.bot.db["conn"]

    def register(self, peer_id):
        sql_str = "INSERT INTO users (user_id, has_vip, banned, has_admin,  prefix) values (%s, false, false, false, default) ON CONFLICT DO UPDATE"
        self.cursor.execute(sql.SQL(sql_str), str(peer_id))
        self.conn.commit()
    def setPrefix(self, user_id: str, prefix) -> None:
        """

        :param user_id:
        :param prefix:
        :return:
        """
        query = f"""
            INSERT INTO public.users (banned, has_admin, has_vip, prefix, user_id)
            values (FALSE, FALSE, FALSE, '{prefix}', '{user_id}')
            ON CONFLICT (user_id) DO UPDATE SET prefix = '{prefix}';
            
            
        """
        self.cursor.execute(query)
        return "ok"
    def returnPrefix(self, user_id: str) -> str:
        """

        :rtype: str
        :param user_id:
        :return:
        """

        query = f"""
            select
                u.prefix
            from
                public.users u
            where u.user_id = {user_id};
            
        """
        try:
            self.cursor.execute(query)
        except Exception as e:
            return e
        return self.cursor.fetchone()
