import sys

import vk_api, logging
from vk_api.exceptions import ApiError
from vk_api.utils import get_random_id
from io import StringIO
import contextlib
from Bot.Plugins.BasePlug import BasePlug


class EvalPlug(BasePlug):
    def __init__(self, bot: object):
        self.bot: object = bot
        self.name = "PythonShell"
        self.description = "Eval your python expressions"
        self.version = "rolling"
        self.keywords = ('eval',)
        self.whoCan = self.bot.admins
        self.onStart()

    def __sendMessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")

    def work(self, peer_id, msg: str, event: vk_api.bot_longpoll.VkBotEvent) -> None:
        if event.obj["from_id"] not in self.bot.admins:
            return

        @contextlib.contextmanager
        def stdoutIO(stdout=None):
            old = sys.stdout
            if stdout is None:
                stdout = StringIO()
            sys.stdout = stdout
            yield stdout
            sys.stdout = old

        code = msg.split(" ", 1)[1]
        with stdoutIO() as s:
            try:
                exec(code)
            except:
                print("Something wrong with the code")
        try:
            self.__sendMessage(peer_id, s.getvalue())
        except ApiError:
            pass
        return
