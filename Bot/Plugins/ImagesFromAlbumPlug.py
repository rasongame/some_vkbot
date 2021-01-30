from vk_api import bot_longpoll
from vk_api.utils import get_random_id

from ..Utils.plug_utils import photo_getWallPhoto
from .BasePlug import BasePlug


class ImagesFromAlbumPlug(BasePlug):
    name = "ImagesFromAlbum"
    description = "Присылает пикчи из разных альбомов"
    keywords = ('каты', "юри", "яой", 'трапы', 'лоли', 'ноги', 'ножки')
    service = {
        "каты": ["-43228812", "каты ебать"],
        "юри": ["-63092480", "Дефки лезбиянки!1!"],
        "лоли": ["-113004231", "лольки бандерольки"],
        "яой": ["-157516431", "педеростня"],
        "трапы": ["-171834188", "девочка с подвохом"],
        "ноги": ["-102853758", "фетишиста ловите блять"],
        "ножги": ["-102853758", "фетишиста ловите блять"],

    }

    def what_needed(self, peer_id, name, count=1):
        attachment = photo_getWallPhoto(self.bot, self.service[name][0], count=count)
        self.bot.send_message(peer_id, self.service[name][1], attachment=attachment)

    def __init__(self, bot):
        super(ImagesFromAlbumPlug, self).__init__(bot)

    def on_start(self):
        pass

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        count = 1
        if self.bot.get_vk_client() == "":
            self.bot.send_message(peer_id, "Эта функция по каким-то причинам не доступна.")
            return

        if len(msg.lower().split()) > 1 and int(msg.lower().split()[1]) <= 10:
            count = msg.lower().split()[1]

        count = int(count)
        try:
            self.what_needed(peer_id, msg.lower().split()[0])
        except:
            # TODO ???
            pass

        return
