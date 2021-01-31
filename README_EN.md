
# Untitled bot
## README IN RUSSIAN HERE [LINK](README.md)
## ALARM! WIP
### Requirements to install
* Python >=3.6
### How to fill a config?
#### Config uses toml format
Basic config with a couple of plugins

```toml
[bot]
token = ""
group_id = ""
client_token = "" # Need for plugin with  ImagesFromAlbumPlug
debug_mode = false
admins = [] # 000000000
plugins = [
    "Bot.Plugins.CorePlug",
    "Bot.Plugins.PluginController"
]
[database]
# Бот использует PostgresSQL в плагине
server = "server.com"
db_name = "db"
port = 5432
user = "postgres"
password = "password"
```

### Install
```shell script
$ cd some_vkbot
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

```

### Start?
```shell script
$ source venv/bin/activate
$ python main.py
```
#### Supports systemd
### 
