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
        # cmds

        if len(event.obj.text) >= 1 and event.from_user or event.obj.text.startswith(prefixs):
            cmd: str = event.obj.text.lower()
            cmd_without_slash: str
            if not event.from_user:
                cmd_without_slash = str(cmd[1:]).split()[0]
                event.obj.text = event.obj.text[1:]
            else:
                if cmd.startswith(prefixs):
                    cmd_without_slash = str(cmd[1:]).split()[0]
                    event.obj.text = event.obj.text[1:]
                else:
                    cmd_without_slash = cmd.split()[0]

            for plug in self.plugins:
                try:
                    if plug.has_keyword(keyword=cmd_without_slash):
                        # logging.info("successful work plugins")
                        logging.info("Поток открылся")
                        if self.get_config()["bot"]['debug_mode']:
                            plug.work(peer_id=event.obj.peer_id, event=event, msg=event.obj.text)
                        else:
                            self.futures.append(
                                self.pool.submit(plug.work, peer_id=event.obj.peer_id, event=event, msg=event.obj.text))
                            self.pool.submit(self.checkThread)
                except IndexError:
                    pass
        # daemon
        daemons = filter(lambda x: x.listen_all is True, self.plugins)
        [plug.work(peer_id=event.obj.peer_id, event=event, msg=event.obj.text) for plug in daemons]
        logging.info(
            f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
