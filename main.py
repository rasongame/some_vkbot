import logging
import sys
from datetime import datetime

import toml

import Bot.Plugins as Plugins
from Bot.bot import Bot
import os.path
from typing import Optional

from Bot.bot_utils import print_info


def generate_config(filename: str) -> Optional[dict]:
    token = input("group token: ")
    group_id = int(input("group id: "))
    if token == "":
        print("токен не указан")
        return
    if group_id <= 0:
        print("id группы должен быть больше или равен 1")
        return

    client_token = input("user access token: ")
    debug_mode = bool(input("debug_mode: "))
    load_only_basic_plugins = bool(input("load only basic plugins? :"))
    cfg = {"bot": {
        "token": token,
        "group_id": group_id,
        "client_token": client_token,
        "debug_mode": debug_mode,
        "load_only_basic_plugins": load_only_basic_plugins,
        "admins": []}}
    with open(filename, 'w') as f:
        toml.dump(cfg, f)
    return cfg


def load_plugins(plugins, bot, only_basic, exclude_list: set[str]):
    """
    Подгрузка всяких плагинов. Nuff said
    :param exclude_list: список плагинов которые не надо загружать
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
        if plugin.name in exclude_list:
            logging.info(f"{plugin.name} in exclude_list")
            plugin.on_stop()
            continue

        plugins.append(plugin)


def main():
    started = datetime.now()
    if not os.path.exists("config/config.toml"):
        generate_config("config/config.toml")
    config = toml.load(open("config/config.toml"))
    plugins = []

    group_id, token = config["bot"]["group_id"], config["bot"]["token"]
    bot = Bot(group_id, token, config)
    exclude_list = config['bot']['exclude_list']
    load_plugins(plugins, bot, config['bot']['load_only_basic_plugins'], exclude_list)
    bot.admins += config["bot"]["admins"]
    bot.plugins += plugins
    # Уиииии, я потом сам не пойму что это за хуйня))))))))
    logging.info(f"Бот запущен за {datetime.now() - started} секунд")
    print_info(bot)
    bot.run()


if __name__ == '__main__':
    main()
