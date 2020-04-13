from Bot.bot import Bot
from Bot.Plugins.CorePlug import CorePlug
from Bot.Plugins.PluginController import PluginController
def main():
    bot = Bot(group_id=184995795, token="ea255b16c9a30b7042427bd2e76d72cb12b98304ee6b762d35633c02a6dcdfbfaad89d8316f033230ad0f")
    bot.plugins.append(CorePlug(bot))
    bot.plugins.append(PluginController(bot))
    bot.admins.append(205479228)
    bot.run()
if __name__ == '__main__':
    main()