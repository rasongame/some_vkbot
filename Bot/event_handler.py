import logging

import vk_api
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType

prefixs = (
    '/',
    '!',
    '.',
    '\\'
)


def event_handler(self, event: VkBotMessageEvent):
    """
    Здесь выполняется обработка эвентов. Nuff said
    :param self:
    :param event:
    :return:

    """
    if event.type == VkBotEventType.MESSAGE_NEW:
        user = {}
        try:
            user = self.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
        except vk_api.exceptions.ApiError:
            user["first_name"] = "bot"
            user["last_name"] = "bot"
        if event.obj.text.startswith(prefixs):
            for plug in self.plugins:
                try:
                    cmd = event.obj.text.lower()
                    cmd_without_slash = str(cmd[1:]).split()[0]
                    if plug.hasKeyword(cmd_without_slash):
                        # logging.info("successful work plugins")
                        logging.info("Поток открылся")
                        if self.config['bot']["debug_mode"]:
                            plug.work(peer_id=event.obj.peer_id, event=event, msg=event.obj.text[1:])
                        else:
                            self.futures.append(
                                self.pool.submit(plug.work, peer_id=event.obj.peer_id, event=event, msg=event.obj.text[1:]))
                            self.pool.submit(self.checkThread)
                except IndexError:
                    pass

        logging.info(
            f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
