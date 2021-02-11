import logging

from .BasePlug import BasePlug


class TestPlug(BasePlug):
    keywords = ['b', ]

    def c(self, event):
        logging.info("a))")

    def b(self, event):
        logging.info("c and b))")

    def __init__(self, bot):
        super().__init__(bot)
        self.register_message_handler(self.c, ("a"))
        self.register_message_handler(self.b, ("c", 'b'))
        self.register_message_handler(self.b, )

    def work(self, peer_id, msg: str, event) -> None:
        if msg.split()[0].removeprefix('/') in self.new_keywords:
            self.new_keywords[msg.split()[0].removeprefix('/')]()
