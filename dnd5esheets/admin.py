"""Definition of admin model views"""

from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import Engine

from .models import Character, Item, Party, Player


class CharacterAdmin(ModelView, model=Character):
    column_list = [
        Character.id,
        Character.name,
        Character.class_,
        Character.level,
        Character.party,
        Character.player,
    ]
    column_details_exclude_list = [
        Character.updated_at,
        Character.created_at,
        Character.player_id,
        Character.party_id,
    ]
    column_labels = {Character.class_: "class"}
    column_searchable_list = [Character.name, Character.class_]


class PartyAdmin(ModelView, model=Party):
    name_plural = "Parties"
    column_list = [Party.id, Party.name, Party.members]
    column_searchable_list = [Party.name]
    column_details_exclude_list = [
        Party.updated_at,
        Party.created_at,
    ]


class PlayerAdmin(ModelView, model=Player):
    column_list = [Player.id, Player.name, Player.email, Player.characters]
    column_searchable_list = [Player.name, Player.email]
    column_details_exclude_list = [
        Player.updated_at,
        Player.created_at,
    ]


class ItemAdmin(ModelView, model=Item):
    page_size = 30
    column_searchable_list = [Item.name]
    column_list = [Item.id, Item.name]
    column_details_exclude_list = [
        Item.updated_at,
        Item.created_at,
    ]


def register_admin(app: FastAPI, engine: Engine) -> Admin:
    admin = Admin(app, engine)
    admin.add_view(CharacterAdmin)
    admin.add_view(PartyAdmin)
    admin.add_view(PlayerAdmin)
    admin.add_view(ItemAdmin)
    return admin
