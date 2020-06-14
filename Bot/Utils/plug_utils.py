import argparse
import random
import time

import requests


def photo_getWallPhoto(self, group_id, albid="wall", count=1):
    max_num = self.vk_client.photos.get(
        owner_id=group_id, album_id=albid, count=0)['count']
    num = random.randint(0, max_num)
    photos = []
    for _ in range(count):
        num = random.randint(0, max_num)
        photo = self.vk_client.photos.get(owner_id=group_id, album_id=albid,
                                          count=1, offset=num)['items'][0]['id']
        photos.append(f"photo{group_id}_{photo}")
    photos = ",".join(photos)
    return photos


def downloadfile(url, expansion="png"):
    name = f"photo{time.time()}.{expansion}"
    with open(name, "wb") as files:
        response = requests.get(url).content
        files.write(response)
    return {"name": name, "expansion": url[-3:]}


class OtherMethod:
    def args(self, text):
        args = argparse.ArgumentParser(description="пикчи")
        args.add_argument("-с", "-c", "--count", type=int, default=1)
        try:
            a = args
            a = a.parse_args(text)
        except:
            try:
                a.count = int(text[0])
            except:
                a.count = 1
        return a

    def photowallrandom(self, text, groups, albid="wall"):
        a = self.args(text[1:])
        photo2 = []
        if a.count > 10:
            a.count = 10
        try:
            for _ in range(a.count):
                group_id = random.choice(groups)
                max_num = self.vk_client.photos.get(
                    owner_id=group_id, album_id=albid, count=0)['count']
                num = random.randint(0, max_num)
                photo = self.vk_client.photos.get(owner_id=group_id, album_id=albid,
                                                  count=1, offset=num)['items'][0]['id']

                photo2.append(f"photo{group_id}_{photo}")
        except KeyboardInterrupt:
            self.sendmsg("!error от вк")
            return
        photo2 = ",".join(photo2)
        return photo2

    def nametoid(self, names):
        uid = []
        for convert in names:
            r = self.vk_client.utils.resolveScreenName(screen_name=convert)
            if r:
                if r["type"] == "group":
                    uid.append(f"-{r['object_id']}")
                else:
                    uid.append(str(r["object_id"]))
            else:
                uid.append(convert)
        return uid

    def randomuser(self):
        whoid = random.choice(self.vk.messages.getConversationMembers(
            peer_id=self.event.object.peer_id)['profiles'])
        whofirstname = whoid['first_name']
        wholastname = whoid['last_name']
        whoidstr = whoid['id']
        return f"@id{whoidstr} ({whofirstname} {wholastname})"

    def groupsearch(self, count, name):
        result = self.vk_client.groups.search(
            q=name, count=count)["items"]
        return ("-" + str(x['id']) for x in result)

    def translit(self, text, lang="ru"):
        apikey = "trnsl.1.1.20190508T201810Z.385ebfa1e596baa0.90672cf8655555b1b51ced31b03c2e8bb9bde46c"
        url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
        params = {"key": apikey,
                  "text": text,
                  "lang": lang}
        r = requests.get(url, params=params, timeout=5)
        encode = r.json()
        return encode["text"][0]
