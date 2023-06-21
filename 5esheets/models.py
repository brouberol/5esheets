import json
from collections import defaultdict

from peewee import CharField, ForeignKeyField, IntegerField, Model, TextField

from .db import db


class BaseModel(Model):
    class Meta:
        database = db


class Player(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Character(BaseModel):
    name = CharField(max_length=255)
    slug = CharField(max_length=255)
    _class = CharField(max_length=80, column_name="class")
    level = IntegerField()
    json_data = TextField()
    player = ForeignKeyField(Player, backref="characters")

    @property
    def data(self):
        d = defaultdict(str)
        d.update(json.loads(self.json_data))
        return d

    def __str__(self):
        return self.name
