from sys import argv

from Bot.Utils.utils import load_class
from Bot.bot import Bot
import toml


def main():
    config = toml.load(open("config/config.toml"))
    plugins = []
    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    pluginPkgs = config["bot"]["plugins"]
    for plug_pkg in pluginPkgs:
        plug_name: str = plug_pkg.split(".")[2]
        cls: object = load_class(f"{plug_pkg}.{plug_name}")
        plugins.append(cls(bot))

    for plugin in plugins:
        bot.plugins.append(plugin)

    for admin in config["bot"]["admins"]:
        bot.admins.append(admin)
    bot.run()


if __name__ == '__main__':
    main()
