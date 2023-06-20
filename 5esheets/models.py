import json
from collections import defaultdict

from peewee import CharField, IntegerField, Model, TextField

from .db import db


class BaseModel(Model):
    class Meta:
        database = db


class Character(BaseModel):
    name = CharField(max_length=255)
    slug = CharField(max_length=255)
    _class = CharField(max_length=80, column_name="class")
    level = IntegerField()
    json_data = TextField()

    class Meta:
        table_name = "character"

    @property
    def data(self):
        d = defaultdict(str)
        d.update(json.loads(self.json_data))
        return d
