import logging

from .BasePlug import BasePlug
from ..event_handler import prefixs

class TestPlug(BasePlug):
    keywords = ['b', ]

    def c(self, event):
        logging.info("a))")

    def b(self, event):
        logging.info("c and b))")

    def __init__(self, bot):
        super().__init__(bot)
        self.register_message_handler(self.c, ("a",))
        self.register_message_handler(self.b, ("c", 'b'))
        self.register_message_handler(self.b, "b")

    def work(self, peer_id, msg: str, event) -> None:
        cmd = ""
        has_prefix = msg.split()[0][0] in prefixs
        if has_prefix:
            cmd = msg.split()[0][1:]
        else:
            cmd = msg.split()[0]

        if cmd in self.new_keywords:
            self.new_keywords[cmd](event)
