"""Definition of admin model views"""

import json
from pathlib import Path
from typing import Type

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from markupsafe import Markup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from sqladmin import Admin, ModelView
from sqladmin.formatters import BASE_FORMATTERS
from sqlalchemy.ext.asyncio import AsyncEngine

from dnd5esheets.models import (
    BaseModel,
    Character,
    EquippedItem,
    Item,
    KnownSpell,
    Party,
    Player,
    Spell,
)

templates_dir = Path(__file__).parent / "templates"
statics_dir = Path(__file__).parent / "statics"


def json_formatter(value: dict) -> Markup:
    json_value = json.dumps(value, indent=2)
    html_json_value = highlight(
        json_value,
        lexer=get_lexer_by_name("json"),
        formatter=HtmlFormatter(),
    )
    return Markup(f"{html_json_value}")


custom_base_formatters = BASE_FORMATTERS | {dict: json_formatter}


def base_excluded_columns(model: Type[BaseModel]):
    return [model.created_at, model.updated_at] + [
        getattr(model, field)
        for field in model.__annotations__
        if field.endswith("_id")
    ]


class CharacterAdmin(ModelView, model=Character):
    column_list = [
        Character.id,
        Character.name,
        Character.class_,
        Character.level,
        Character.party,
        Character.player,
    ]
    column_details_exclude_list = base_excluded_columns(Character)
    form_excluded_columns = base_excluded_columns(Character)
    column_labels = {Character.class_: "class"}
    column_searchable_list = [Character.name, Character.class_]
    column_type_formatters = custom_base_formatters
    details_template = "details_custom.html"


class PartyAdmin(ModelView, model=Party):
    name_plural = "Parties"
    column_list = [Party.id, Party.name, Party.members]
    column_searchable_list = [Party.name]
    column_details_exclude_list = base_excluded_columns(Party)
    form_excluded_columns = base_excluded_columns(Party)


class PlayerAdmin(ModelView, model=Player):
    column_list = [Player.id, Player.name, Player.email, Player.characters]
    column_searchable_list = [Player.name, Player.email]
    column_details_exclude_list = base_excluded_columns(Player) + [
        Player.hashed_password
    ]
    form_excluded_columns = base_excluded_columns(Player) + [Player.hashed_password]


class ItemAdmin(ModelView, model=Item):
    page_size = 30
    column_searchable_list = [Item.name]
    column_list = [Item.id, Item.name]
    column_details_exclude_list = base_excluded_columns(Item)
    form_excluded_columns = base_excluded_columns(Item)
    column_type_formatters = custom_base_formatters


class EquippedItemAdmin(ModelView, model=EquippedItem):
    column_list = [
        EquippedItem.id,
        EquippedItem.owner,
        EquippedItem.item,
        EquippedItem.amount,
        EquippedItem.equipped,
    ]
    column_details_exclude_list = base_excluded_columns(EquippedItem)
    form_excluded_columns = base_excluded_columns(EquippedItem)


class KnownSpellAdmin(ModelView, model=KnownSpell):
    column_list = [
        KnownSpell.id,
        KnownSpell.caster,
        KnownSpell.spell,
        KnownSpell.prepared,
    ]


class SpellAdmin(ModelView, model=Spell):
    page_size = 30
    column_searchable_list = [Spell.name, Spell.level]
    column_list = [Spell.id, Spell.name, Spell.level, Spell.school]
    column_details_exclude_list = base_excluded_columns(Spell)
    form_excluded_columns = base_excluded_columns(Spell)
    column_sortable_list = [Spell.name, Spell.level]
    column_type_formatters = custom_base_formatters


def register_admin(app: FastAPI, engine: AsyncEngine) -> Admin:
    admin = Admin(app, engine, title="5esheets admin", templates_dir=str(templates_dir))
    app.mount(
        "/admin-statics",
        StaticFiles(directory=statics_dir, html=True),
        name="admin_statics",
    )
    # Automatically discover admin views in current module
    views = list(
        {
            k: v
            for k, v in globals().items()
            if k.endswith("Admin")
            if k != "Admin"
            if issubclass(v, ModelView)
        }.values()
    )

    views = sorted(views, key=lambda view: view.model.__name__)
    for view in views:
        admin.add_view(view)
    return admin
