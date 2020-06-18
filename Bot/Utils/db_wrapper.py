from peewee import *

database = Proxy()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Example(BaseModel):
    author_id = IntegerField(null=True)
    message = TextField(null=True)

    class Meta:
        table_name = 'example'


class User(BaseModel):
    has_admin = BooleanField()
    has_banned = BooleanField()
    has_vip = BooleanField()
    prefix = CharField()
    user_id = IntegerField()

    class Meta:
        table_name = 'user'


class Chats(BaseModel):
    chat_id = IntegerField()

    class Meta:
        table_name = "chats"


class Users(BaseModel):
    banned = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    has_admin = BooleanField(constraints=[SQL("DEFAULT false")])
    has_vip = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    prefix = CharField(null=True)
    user_id = IntegerField()

    class Meta:
        table_name = 'users'
