"""Definition of admin model views"""

from pathlib import Path
from typing import Type

import orjson
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from markupsafe import Markup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from sqladmin import Admin, ModelView
from sqladmin.authentication import login_required
from sqladmin.formatters import BASE_FORMATTERS
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response

from dnd5esheets.models import (
    BaseModel,
    Character,
    EquippedItem,
    Item,
    KnownSpell,
    Party,
    Player,
    PlayerRole,
    Spell,
)

templates_dir = Path(__file__).parent / "templates"
statics_dir = Path(__file__).parent / "statics"


def json_formatter(value: dict) -> Markup:
    json_value = orjson.dumps(value, option=orjson.OPT_INDENT_2)
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
    column_list = [
        Player.id,
        Player.name,
        Player.email,
        Player.characters,
        Player.player_roles,
    ]
    column_searchable_list = [Player.name, Player.email]
    column_details_exclude_list = base_excluded_columns(Player) + [
        Player.hashed_password
    ]
    form_excluded_columns = base_excluded_columns(Player) + [Player.hashed_password]
    column_labels = {Player.player_roles: "roles"}


class ItemAdmin(ModelView, model=Item):
    page_size = 30
    column_searchable_list = [Item.name]
    column_list = [Item.id, Item.name]
    column_details_exclude_list = base_excluded_columns(Item)
    form_excluded_columns = base_excluded_columns(Item)
    column_type_formatters = custom_base_formatters
    details_template = "details_custom.html"


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
    _column_formatters = {
        Spell.school: lambda model, _: model.school.capitalize(),  # type: ignore
    }

    page_size = 30
    column_searchable_list = [Spell.name, Spell.level]
    column_list = [Spell.id, Spell.name, Spell.level, Spell.school]
    column_details_exclude_list = base_excluded_columns(Spell)
    form_excluded_columns = base_excluded_columns(Spell)
    column_sortable_list = [Spell.name, Spell.level]
    column_type_formatters = custom_base_formatters
    details_template = "details_custom.html"
    column_formatters_detail = _column_formatters  # type: ignore
    column_formatters = _column_formatters  # type: ignore


class PlayerRoleAdmin(ModelView, model=PlayerRole):
    column_list = [
        PlayerRole.id,
        PlayerRole.party,
        PlayerRole.player,
        PlayerRole.role,
    ]
    column_details_exclude_list = base_excluded_columns(PlayerRole)
    form_excluded_columns = base_excluded_columns(PlayerRole)


class CustomAdmin(Admin):
    @login_required
    async def index(self, _: Request) -> Response:
        """Redirect admin index page to the listing of the first model view"""
        return RedirectResponse(url=f"{self.views[0].identity}/list")


def register_admin(app: FastAPI, engine: AsyncEngine) -> Admin:
    admin = CustomAdmin(
        app, engine, title="5esheets admin", templates_dir=str(templates_dir)
    )
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
