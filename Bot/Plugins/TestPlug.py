from .BasePlug import BasePlug


class TestPlug(BasePlug):

    def __init__(self, bot):
        super().__init__(bot)

    def work(self, peer_id, msg: str, event) -> None:
        cmd = self.get_cmd_from_msg(msg)
        if cmd in self.keywords:
            self.keywords[cmd](peer_id, msg, event)
