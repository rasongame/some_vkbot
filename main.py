from Bot.bot import Bot
from Bot.Plugins.CorePlug import CorePlug
from Bot.Plugins.PluginController import PluginController
from sys import argv
def main():
    bot = Bot(group_id=argv[1], token=argv[2])
    bot.plugins.append(CorePlug(bot))
    bot.plugins.append(PluginController(bot))
    bot.admins.append(205479228)
    bot.run()
if __name__ == '__main__':
    main()