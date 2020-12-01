import peewee


class db_handler:
    db = peewee.DatabaseProxy()

    def __init__(self, file_name):
        self.db.initialize(peewee.SqliteDatabase(file_name))
        print(self.db)


class User(peewee.Model):
    id = peewee.IntegerField(unique=True)
    bg_file_name = peewee.CharField()

    class Meta:
        database = db_handler.db
