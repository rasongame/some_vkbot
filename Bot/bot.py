import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import logging


class Bot:
    def __init__(self, group_id, token) -> None:
        self.group_id = group_id
        self.token = token
        self.version = "Rolling Version"
        self.vk: vk_api.VkApi = vk_api.VkApi(token=self.token)
        self.longpoll: VkBotLongPoll = VkBotLongPoll(self.vk, self.group_id)
        self.plugins = []
        self.disabledPlugins = []
        self.admins = []
        logging.basicConfig(level=logging.INFO, format=" [ %(filename)s # %(levelname)-8s %(asctime)s ]  %(message)-2s")

    def run(self) -> None:
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                logging.info(f"{event.message.from_id} in {event.message.peer_id} send: {event.message.text}")
                for plug in self.plugins:
                    try:
                        if event.message.text.split()[0] in plug.keywords:
                            logging.info("successfull work plugins")
                            plug.work(event.message.peer_id, event.message.text, event)
                    except IndexError:
                        pass
