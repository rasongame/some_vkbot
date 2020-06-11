from vk_api import bot_longpoll, VkUpload
from vk_api.utils import get_random_id
from ..bot import Bot
from ..Utils.plug_utils import photo_getWallPhoto


class ImagesFromAlbumPlug:
    name = "ImagesFromAlbum"
    description = "Присылает пикчи из разных альбомов"
    version = "rolling"
    keywords = ('каты', "юри", "яой", 'трапы', 'лоли', 'ноги', 'ножки')
    whoCan = ''
    event_type = ""
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

        self.onStart()

    def Cats_cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-43228812", count=count)
        self.__sendMessage_with_img(peer_id, "каты ебать", attachment=attachment)

    def Yuri_Cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-63092480", count=count)
        self.__sendMessage_with_img(peer_id, "Дефки лезбиянки!1!", attachment=attachment)

    def Yaoi_Cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-113004231", count=count)
        self.__sendMessage_with_img(peer_id, "педеростня", attachment=attachment)

    def Loli_Cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-157516431", count=count)
        self.__sendMessage_with_img(peer_id, "лольки бандерольки", attachment=attachment)

    def Traps_Cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-171834188", count=count)
        self.__sendMessage_with_img(peer_id, "девочка с подвохом", attachment=attachment)

    def FootFetish_Cmd(self, text, peer_id: int, count=1):
        attachment = photo_getWallPhoto(self.bot, "-102853758", count=count)
        self.__sendMessage_with_img(peer_id, "фетишиста ловите блять", attachment=attachment)

    def __sendMessage_with_img(self, peer_id: int, msg: str, attachment: str = "") -> None:
        return self.bot.vk.method("messages.send",
                                  {"peer_id": peer_id, "message": msg, "random_id": get_random_id(),
                                   'attachment': attachment})

    def onStart(self):
        pass

    def hasKeyword(self, keyword: str) -> bool:
        return keyword in self.keywords

    def work(self, peer_id: int, msg: str, event: bot_longpoll.VkBotEvent) -> None:
        count = 1
        if len(msg.lower().split()) > 1 and int(msg.lower().split()[1]) <= 10:
            count = msg.lower().split()[1]

        count = int(count)
        if msg.lower().split()[0] == "каты":
            self.Cats_cmd(msg, peer_id, count=count)
        elif msg.lower().split()[0] == "юри":
            self.Yuri_Cmd(msg, peer_id, count=count)
        elif msg.lower().split()[0] == "яой":
            self.Yaoi_Cmd(msg, peer_id, count=count)
        elif msg.lower().split()[0] == "лоли":
            self.Loli_Cmd(msg, peer_id, count=count)
        elif msg.lower().split()[0] == "трапы":
            self.Traps_Cmd(msg, peer_id, count=count)
        elif msg.lower().split()[0] == "ноги" or msg.lower().split()[0] == "ножки":
            self.FootFetish_Cmd(msg, peer_id, count=count)
        else:
            pass

        return
