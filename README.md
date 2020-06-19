
# Безымянный бот
### Требования к установке
* Python 3.6 (а может и ниже, я не проверял)
* PostgreSQL, если необходима работа с БД, пока это еще захардкожено в коде
* 
### Как заполнить конфиг?
#### Конфиг использует формат TOML
Базовый конфиг с парой плагинов

```toml
[bot]
token = ""
group_id = ""
client_token = "" # Необходимо для плагина ImagesFromAlbumPlug
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

### Установка
```shell script
$ cd some_vkbot
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
###
### 