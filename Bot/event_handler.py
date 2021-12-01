import logging

import vk_api
from vk_api.bot_longpoll import VkBotMessageEvent, VkBotEventType, VkBotEvent

PREFIXS = (
    '/',
    '!',
    '.',
    '\\'
)


def message_new_event_handler(self, event: VkBotMessageEvent):
    if event.message.text == "/": return # пропуск бесполезных слешей для избежания IndexError
    if event.from_user or event.message.text.startswith(PREFIXS):
        cmd: str = event.message.text.lower()
        cmd_without_slash = str(cmd[1:]).split()[0]
        if event.from_user:
            if cmd.startswith(PREFIXS):
                event.message.text = event.message.text[1:]
            else:
                cmd_without_slash = cmd.split()[0]

        for plug in self.plugins:
            try:
                if plug.has_keyword(keyword=cmd_without_slash):
                    # logging.info("successful work plugins")
                    logging.info("Поток открылся")
                    if self.is_debug:
                        plug.work(peer_id=event.message.peer_id, event=event, msg=event.message.text)
                    else:
                        self.futures.append(
                            self.pool.submit(plug.work, peer_id=event.message.peer_id, event=event, msg=event.message.text))
                        self.pool.submit(self.checkThread)

                    break
            except IndexError:
                pass
    # daemon
    daemons = filter(lambda x: x.listen_all is True, self.plugins)
    [plug.work(peer_id=event.message.peer_id, event=event, msg=event.message.text) for plug in daemons]
    logging.info(
        f'{event.message.from_id} in {event.message.peer_id} sent: {event.message.text}')


def group_event_handler(self, event: VkBotEvent):
    joined = "Присоединился" if event.type == VkBotEventType.GROUP_JOIN else "Покинул"
    kicked = False
    if joined == "Покинул":
        kicked = "кикнут" if not bool(event.message.self) else "вышел самостоятельно"
    text = f"""
    {joined} {event.message.user_id}
    {"Причина: " + kicked if joined == "Покинул" else ""}
    """
    [self.send_message(admin, text) for admin in self.get_config()['bot']['admins']]


def event_handler(self, event: VkBotEvent):
    """
    Здесь выполняется обработка эвентов. Nuff said
    :param self:
    :param event:
    :return:

    """
    type = event.type
    if type == VkBotEventType.MESSAGE_NEW:
        message_new_event_handler(self, event)
    elif type in (VkBotEventType.GROUP_JOIN, VkBotEventType.GROUP_LEAVE):
        group_event_handler(self, event)
