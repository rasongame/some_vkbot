import logging

from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class JoinPlug(BasePlug):
    name = "GroupJoinPlug"
    description = "Приветствие при входе в группу"
    version = "rolling"
    keywords = ('',)
    whoCan = ''
    event_type = ("chat_kick_user",)

    def __init__(self, bot: object):
        self.bot: object = bot
        self.onStart()



    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def work(self, event, **kwargs) -> None:
        if event.obj.action['type'] == self.event_type[0]:
            self.__sendMessage(peer_id=event.obj.peer_id, msg=f"он был великим человеком, земля ему кирпичной кладкой")

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")
