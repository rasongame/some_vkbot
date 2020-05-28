

def shell(bot, peer_id, msg):
    bot.vk.method("messages.send", {"peer_id": peer_id, "message": msg})
    return