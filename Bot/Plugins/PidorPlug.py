import random

from vk_api import bot_longpoll
from vk_api import exceptions
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class PidorPlug(BasePlug):
    name = "Pidor"
    description = "Выбирает рандомного участника беседы под вашим предлогом"
    keywords = ('who', 'кто')

    def __init__(self, bot):
        super(self.__class__, self).__init__(bot)


    def __send_message(self, peer_id: int, msg: str) -> None:
        self.bot.vk.method("messages.send",
                           {"disable_mentions": 1, "peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent):
        if len(msg.split()) >= 2:

            who = msg.split(maxsplit=1)[1]
        else:
            self.__send_message(peer_id, "Ты что-то упустил...")
            return

        try:
            s = self.bot.vk.method("messages.getConversationMembers",
                                   {"peer_id": peer_id, "group_id": self.bot.group_id})
            chosen = random.choice(s["items"])
            first_name, last_name = "", ""
            if str(chosen["member_id"]).startswith("-"):
                user = self.bot.vk.get_api().groups.getById(group_ids=chosen["member_id"])[0]
                first_name = user["name"]
                last_name = ""
                self.__send_message(peer_id, f'Пидор - [{user["screen_name"]}|{first_name} {last_name}]')
            else:

                user = self.bot.vk.get_api().users.get(user_ids=chosen["member_id"])[0]

                first_name = user["first_name"]
                last_name = user["last_name"]
                self.__send_message(peer_id, f'Кто - {who}? Я думаю это [id{user["id"]}|{first_name} {last_name}]')

        except exceptions.ApiError as e:
            self.__send_message(peer_id,
                               f"""
                            Команда не доступна для этого чата. Код ошибки {e.code}
                            Вероятно, у бота нет привилегий в чате.
                            Как решить? Выдайте боту админку.
                                """)
        #

        return
