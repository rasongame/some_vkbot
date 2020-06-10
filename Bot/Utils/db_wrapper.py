import peewee


class BaseModel(peewee.Model):
    def __init__(self, db=None):
        self.database = db

class User(BaseModel):
    # def __init__(self, db=None, ):
    user_id = peewee.IntegerField()
    has_banned = peewee.BooleanField()
    has_vip = peewee.BooleanField()
    has_admin = peewee.BooleanField()
    prefix = peewee.CharField()
    id = peewee.AutoField()

