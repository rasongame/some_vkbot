import contextlib
import logging
import sys
from io import StringIO

import vk_api
from vk_api.exceptions import ApiError
from vk_api.utils import get_random_id

from Bot.Plugins.BasePlug import BasePlug


class EvalPlug(BasePlug):
    name = "PythonShell"
    description = "Eval your python expressions"
    version = "rolling"
    keywords = ('eval',)
    event_type = ""

    def __init__(self, bot: object):
        super(EvalPlug, self).__init__(bot)
        self.whoCan = bot.admins

    def __sendmessage(self, peer_id, msg):
        self.bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg, "random_id": get_random_id()})

    def on_start(self) -> None:
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
            except Exception as e:
                print(f"Something wrong with the code: {e}")
        try:
            self.__sendmessage(peer_id, s.getvalue())
        except ApiError:
            pass
        return
