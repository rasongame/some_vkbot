import logging
from datetime import datetime

import toml

import Bot.Plugins as Plugins
from Bot.bot import Bot


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
