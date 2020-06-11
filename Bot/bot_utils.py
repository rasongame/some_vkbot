from vk_api.bot_longpoll import VkBotEventType, VkBotMessageEvent
import logging
import vk_api


def eventHandler(self, event: VkBotMessageEvent):
    #     if event.type == VkBotEventType.MESSAGE_EDIT:
    #         for plug in self.plugins:
    #             try:
    #                 if plug.event_type == VkBotEventType.MESSAGE_EDIT

    if event.type == VkBotEventType.MESSAGE_NEW:
        user = {}
        # if event.obj.action is not None and len(event.obj.action) >= 1:
        #     plug = [x for x in self.plugins if event.obj.action['type'] in x.event_type][0]
        #     print(plug.name)
        #     plug.work(event)
        #     return
        #
        try:
            user = self.vk.get_api().users.get(user_ids=event.obj.from_id)[0]
        except vk_api.exceptions.ApiError:
            user["first_name"] = "bot"
            user["last_name"] = "bot"
        for plug in self.plugins:
            try:
                if plug.hasKeyword(event.obj.text.lower().split()[0]):
                    # logging.info("successfull work plugins")
                    logging.info("Поток открылся")
                    if self.config['bot']["debug_mode"] == True:
                        plug.work(event.obj.peer_id, event.obj.text, event)
                    else:
                        self.futures.append(self.pool.submit(plug.work, event.obj.peer_id, event.obj.text, event))
                        self.pool.submit(self.checkThread)
            except IndexError:
                pass
        logging.info(
            f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
