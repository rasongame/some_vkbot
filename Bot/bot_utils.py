from vk_api.bot_longpoll import VkBotEventType, VkBotMessageEvent
import logging
import vk_api


def eventHandler(self, event: VkBotMessageEvent):
    if event.type == VkBotEventType.MESSAGE_NEW:
        user = {}
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
        
        logging.info(f'{user["first_name"]} {user["last_name"]}({event.obj.from_id}) in {event.obj.peer_id} sent: {event.obj.text}')
