from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from .BasePlug import BasePlug
from .CorePlug_utils.common import *
from .CorePlug_utils.debug import *


class CorePlug(BasePlug):
    description = "Корневой плагин бота"
    is_basic = True

    def __init__(self, bot):
        super().__init__(bot)
        self.register_message_handler(print_help, ['хелп', 'help', 'помощь'])
        self.register_message_handler(print_info, ['info', 'инфо'])
        self.register_message_handler(print_start_info, ['начать', 'start'])
        self.register_message_handler(send_report, ['репорт', 'репорт'])
        self.register_message_handler(print_live, ['ping', 'пинг', "жив?"])
        self.register_message_handler(print_debug, ['debug', 'дебаг'])
        self.register_message_handler(print_json, ['json'])
