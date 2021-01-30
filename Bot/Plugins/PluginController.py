from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from .BasePlug import BasePlug


class PluginController(BasePlug):
    name = "Plugin Controller"
    description = "Plugin controller"
    keywords = ('disable', 'enable')

    def __init__(self, bot):
        super(self.__class__, self).__init__(bot)


    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent):
        if event.obj.from_id in self.bot.admins:
            if msg.lower().split()[0] == self.keywords[0]:
                try:
                    self.bot.disabledPlugins.append(self.bot.plugins.pop(int(msg.split()[1])))
                    plugin = self.bot.plugins[(int(msg.split()[1]))]
                    plugin.on_stop()
                    self.bot.send_message(peer_id=peer_id, msg="Plugin disabled!")
                    self.bot.send_message(peer_id=peer_id, msg=self.bot.disabledPlugins)
                except IndexError:
                    self.bot.send_message(peer_id, "You tried to disable of NULL plugin? You baka")
            elif msg.lower().split()[0] == self.keywords[1]:
                try:
                    self.bot.plugins.append(self.bot.disabledPlugins.pop(int(msg.split()[1])))
                    plugin = self.bot.plugins[(int(msg.split()[1]))]
                    plugin.on_start()
                    self.bot.send_message(peer_id, f"Plugin enabled")
                    # {self.bot.plugins}
                    # prepared_msg = self.bot.plugins
                except IndexError:
                    self.bot.send_message(peer_id, "You tryed to enable of NULL plugin? You baka")
                    self.bot.send_message(peer_id=peer_id, msg=self.bot.plugins)
        else:
            self.bot.send_message(peer_id, "Братка... Ты зачем пукнул в трусы?")
