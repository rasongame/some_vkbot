import logging
from datetime import datetime

import toml

import Bot.Plugins as Plugins
from Bot.bot import Bot
import os.path


def generate_config(filename: str) -> dict:
    token = input("group token: ")
    group_id = int(input("group id: "))
    client_token = input("user access token: ")
    debug_mode = bool(input())
    cfg = {"bot": {
        "token": token,
        "group_id": group_id,
        "client_token": client_token,
        "debug_mode": debug_mode,
        "admins": []}}

    return cfg


def load_plugins(plugins, bot, only_basic):
    """
    Подгрузка всяких плагинов. Nuff said
    :param only_basic: Загрузить только CorePlug/другие плагины с is_basic=True атрибутом
    :param plugins:
    :param bot:
    :return:
    """
    x = dir(Plugins)
    for cls in x:
        attribute = getattr(Plugins, cls)
        if attribute is None or not hasattr(attribute, cls):
            continue
        raw = getattr(attribute, cls)
        if only_basic and not raw.is_basic:
            continue

        plugin: Plugins.BasePlug = raw(bot)
        plugins.append(plugin)


def main():
    started = datetime.now()
    if not os.path.exists("config/config.toml"):
        cfg = generate_config("config/config.toml")
        with open("config/config.toml", 'w') as f:
            new = toml.dump(cfg, f)
            print(new)
    config = toml.load(open("config/config.toml"))
    plugins = []

    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    load_plugins(plugins, bot, config['bot']['load_only_basic_plugins'])
    bot.admins += config["bot"]["admins"]
    bot.plugins += plugins
    # Уиииии, я потом сам не пойму что это за хуйня))))))))
    logging.info(f"Бот запущен за {datetime.now() - started} секунд")
    bot.run()


if __name__ == '__main__':
    main()
