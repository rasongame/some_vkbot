import logging
from datetime import datetime

import toml
from inspect import ismodule

from Bot.Plugins import BasePlug
from Bot.bot import Bot
import Bot.Plugins as Plugins


def load_plugins(plugins, bot):
    """
    Подгрузка всяких плагинов. Nuff said
    :param plugins:
    :param bot:
    :return:
    """
    for cls in dir(Plugins):
        attribute = getattr(Plugins, cls)
        if attribute is None or not hasattr(attribute, cls): continue
        plugins.append(getattr(attribute, cls)(bot))

    #
    # plug_name: str = plug_pkg.split(".")[2]
    # cls = load_class(f"{plug_pkg}.{plug_name}")
    #
    # plugins.append(cls(bot))


def main():
    started = datetime.now()
    config = toml.load(open("config/config.toml"))
    plugins = []

    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    load_plugins(plugins, bot)
    bot.admins += config["bot"]["admins"]
    bot.plugins += plugins
    # Уиииии, я потом сам не пойму что это за хуйня))))))))
    logging.info(f"Бот запущен за {datetime.now() - started} секунд")
    bot.run()


if __name__ == '__main__':
    main()
