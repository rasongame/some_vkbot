import random

from vk_api import bot_longpoll
from vk_api import exceptions
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class PidorPlug(BasePlug):
    name = "Pidor"
    description = "Выбирает рандомного участника беседы"
    keywords = ('who', 'кто')

    def __init__(self, bot):
        super(self.__class__, self).__init__(bot)

    def get_members(self, peer_id: int):
        s = self.bot.vk.method("messages.getConversationMembers",
                               {"peer_id": peer_id, "group_id": self.bot.group_id})
        return random.choice(s["items"])

    def select_member(self, peer_id: int, member_id: int):
        """

        :param peer_id:
        :param member_id:
        :return: member_info: dict, is_public: bool

        """
        api = self.bot.vk.get_api()
        if member_id < 0: # используем метод groups.getById для групп.
            return api.groups.getById(groups_is=member_id)[0], True
        else:
            return api.users.get(user_ids=member_id)[0], False

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent):
        if len(msg.split()) >= 2:
            who = msg.split(maxsplit=1)[1]
        else:
            self.bot.send_message(peer_id, "Ты что-то упустил...")
            return

        try:
            chosen = self.get_members(peer_id)
            member, is_public = self.select_member(peer_id, chosen['member_id'])
            id = member['screen_name'] if is_public else f"id{member['id']}"
            name = member['name'] if is_public else f'{member["first_name"]} {member["last_name"]}'
            self.bot.send_message(peer_id, f'Кто {who}? Возможно это [{id}|{name}]!')


        except exceptions.ApiError as e:
            self.bot.send_message(peer_id,
                                  f"""
                            Команда не доступна для этого чата. Код ошибки {e.code}
                            Вероятно, у бота нет привилегий в чате.
                            Как решить? Выдайте боту админку.
                                """)
        #

        return
