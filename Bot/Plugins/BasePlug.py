from ..bot import Bot
import logging
class BasePlug:
    def __init__(self, bot):
        self.bot: Bot = bot
        self.name = "some name"
        self.description = "some description"
        self.version = "rolling"
        self.keywords = ['']
        self.whoCan = ''
        self.onStart()

    def work(self) -> None:
        pass
    def onStart(self) -> None:
        logging.info(f"{self.name} is loaded")
    def onStop(self) -> None:
        logging.info(f"{self.name} is disabling")