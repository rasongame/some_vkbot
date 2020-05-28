from sys import argv

from Bot.Utils.utils import load_class
from Bot.bot import Bot
import toml, logging
from datetime import datetime
def loadPlugins(plug_pkg, plugins, bot):
    plug_name: str = plug_pkg.split(".")[2]
    cls: object = load_class(f"{plug_pkg}.{plug_name}")
    plugins.append(cls(bot))

def main():
    started = datetime.now()
    config = toml.load(open("config/config.toml"))
    plugins = []
    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    pluginPkgs = config["bot"]["plugins"]
    # for plug_pkg in pluginPkgs:
    [loadPlugins(plug_pkg, plugins, bot) for plug_pkg in pluginPkgs]
    bot.plugins = [plugin for plugin in plugins]
    bot.admins = [admin for admin in config["bot"]["admins"]]
    # Уиииии, я потом сам не пойму что это за хуйня))))))))
    logging.info(f"Бот запущен за {datetime.now() - started} секунд")
    bot.run()


if __name__ == '__main__':
    main()
