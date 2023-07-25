"""Definition of admin model views"""

from typing import Type

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Engine

from .models import BaseModel, Character, Item, Party, Player


def base_excluded_columns(model: Type[BaseModel]):
    return [model.created_at, model.updated_at]


class CharacterAdmin(ModelView, model=Character):
    column_list = [
        Character.id,
        Character.name,
        Character.class_,
        Character.level,
        Character.party,
        Character.player,
    ]
    column_details_exclude_list = base_excluded_columns(Character) + [
        Character.player_id,
        Character.party_id,
    ]
    form_excluded_columns = base_excluded_columns(Character)
    column_labels = {Character.class_: "class"}
    column_searchable_list = [Character.name, Character.class_]


class PartyAdmin(ModelView, model=Party):
    name_plural = "Parties"
    column_list = [Party.id, Party.name, Party.members]
    column_searchable_list = [Party.name]
    column_details_exclude_list = base_excluded_columns(Party)
    form_excluded_columns = base_excluded_columns(Party)


class PlayerAdmin(ModelView, model=Player):
    column_list = [Player.id, Player.name, Player.email, Player.characters]
    column_searchable_list = [Player.name, Player.email]
    column_details_exclude_list = base_excluded_columns(Player)
    form_excluded_columns = base_excluded_columns(Player) + [Player.hashed_password]


class ItemAdmin(ModelView, model=Item):
    page_size = 30
    column_searchable_list = [Item.name]
    column_list = [Item.id, Item.name]
    column_details_exclude_list = base_excluded_columns(Item)
    form_excluded_columns = base_excluded_columns(Item)


def register_admin(app: FastAPI, engine: Engine) -> Admin:
    admin = Admin(app, engine)
    admin.add_view(CharacterAdmin)
    admin.add_view(PartyAdmin)
    admin.add_view(PlayerAdmin)
    admin.add_view(ItemAdmin)
    return admin
