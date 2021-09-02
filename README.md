
# Безымянный бот aka исходники vk.com/mtt_resort с июня 2020 
## WIP.. На дороге к релизу, крч.

### Требования
* Python >=3.6
### Как заполнить конфиг?
#### Конфиг использует формат TOML
Базовый конфиг

```toml
[bot]
token = ""
group_id = ""
client_token = "" # Необходимо для плагина ImagesFromAlbumPlug
debug_mode = false
admins = [] # 000000000

```

### Установка
```shell script
$ cd some_vkbot
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

```

### Запуск?
```shell script
$ source venv/bin/activate
$ python main.py
```
#### Есть поддержка systemd
### 
