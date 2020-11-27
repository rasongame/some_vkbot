import logging
from datetime import datetime

import toml

from Bot.Utils.utils import load_class
from Bot.bot import Bot


def loadPlugins(plug_pkg, plugins, bot):
    """
    Подгрузка всяких плагинов. Nuff said
    :param plug_pkg:
    :param plugins:
    :param bot:
    :return:
    """
    plug_name: str = plug_pkg.split(".")[2]
    cls = load_class(f"{plug_pkg}.{plug_name}")
    plugins.append(cls(bot))


def main():
    started = datetime.now()
    config = toml.load(open("config/config.toml"))
    plugins = []

    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    plugins_packages = config["bot"]["plugins"]
    [loadPlugins(plug_pkg, plugins, bot) for plug_pkg in plugins_packages]
    bot.admins += config["bot"]["admins"]
    bot.plugins += plugins
    # Уиииии, я потом сам не пойму что это за хуйня))))))))
    logging.info(f"Бот запущен за {datetime.now() - started} секунд")
    bot.run()


if __name__ == '__main__':
    main()
