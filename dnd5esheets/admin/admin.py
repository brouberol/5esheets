"""Definition of admin model views"""

from pathlib import Path
from typing import Any, Coroutine, Type

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
from dnd5esheets.schemas import CharacterSheet

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


def link(url: str, title: str | None = None) -> Markup:
    return Markup(f"<a href='{url}'>{title or url}</a>")


custom_base_formatters = BASE_FORMATTERS | {dict: json_formatter}


def base_excluded_columns(model: Type[BaseModel]) -> list:
    """Hide the id, creation/update dates and foreign key fields by default"""
    excluded_base_columns = [model.id, model.created_at, model.updated_at]
    foreign_keys = [getattr(model, field) for field in model.__annotations__ if field.endswith("_id")]
    return excluded_base_columns + foreign_keys


def base_form_excluded_columns(model: Type[BaseModel]) -> list:
    """Exclude hidden fields from form"""
    return base_excluded_columns(model)


class CustomModelView(ModelView):
    """A ModelView allowing the mixing of SQLAlchemy columns and model properties"""

    details_property_exclude_list: list[str] = []

    def get_details_columns(self) -> list[str]:
        """Get list of properties to display in Detail page."""

        column_details_list = getattr(self, "column_details_list", None)

        # Automatically inject model properties along with model SQLAlchemy columns
        property_details_list = [
            col
            for col in dir(self.model)
            if not col.startswith("_")
            if col not in self.details_property_exclude_list
            if hasattr(getattr(self.model, col), "fset")
        ]
        self._prop_names += property_details_list
        # End of custom code

        column_details_exclude_list = getattr(self, "column_details_exclude_list", None)
        return self._build_column_list(
            include=column_details_list,
            exclude=column_details_exclude_list,
            defaults=self._prop_names,
        )


def render_json_data(value):
    """This filter is called when rendering a JSON value.

    As we're going back and forth between dict (in python) and JSON (in database),
    we need to make sure that we display valid JSON-encoded data in the form widget.
    If we don't (eg if we display a python dict repr), we will then JSON-encode a string
    in database, which won't be a valid JSON object anymore, and all hell breaks loose.

    """
    if isinstance(value, dict):
        json_value = orjson.dumps(value).decode("utf-8")
        return json_value
    return value


class CharacterAdmin(ModelView, model=Character):
    column_list = [
        Character.id,
        Character.name,
        "level",  # This is a property, not an SQLAlchemy mapped column
        "classes_repr",  # Same
        Character.party,
        Character.player,
    ]
    column_details_exclude_list = base_excluded_columns(Character)
    form_excluded_columns = base_form_excluded_columns(Character)
    form_args = dict(data=dict(filters=[render_json_data]))
    column_searchable_list = [Character.name]
    column_type_formatters = custom_base_formatters
    details_template = "details_custom.html"

    def insert_model(self, request: Request, data) -> Coroutine[Any, Any, Any]:
        """Insert a new Character with an empty CharacterSheet model if no data is specified."""
        data_str = data.get("data")
        if not data_str:
            data_str = orjson.dumps(CharacterSheet.model_validate({}).model_dump()).decode("utf-8")
        data["data"] = data_str
        return super().insert_model(request, data)


class PartyAdmin(ModelView, model=Party):
    name_plural = "Parties"
    column_list = [Party.id, Party.name, Party.members]
    column_searchable_list = [Party.name]
    column_details_exclude_list = base_excluded_columns(Party)
    form_excluded_columns = base_form_excluded_columns(Party)


class PlayerAdmin(ModelView, model=Player):
    column_list = [
        Player.id,
        Player.name,
        Player.email,
        Player.characters,
        Player.player_roles,
    ]
    column_searchable_list = [Player.name, Player.email]
    column_details_exclude_list = base_excluded_columns(Player) + [Player.hashed_password]
    form_excluded_columns = base_form_excluded_columns(Player) + [Player.hashed_password]
    column_labels = {Player.player_roles: "roles"}


class ItemAdmin(CustomModelView, model=Item):
    _column_formatters = {
        "five_e_tools_url": lambda model, _: link(model.five_e_tools_url),
    }
    column_labels = {"five_e_tools_url": "5e.tools URL"}
    page_size = 30
    column_searchable_list = [Item.name]
    column_list = [Item.id, Item.name]
    column_details_exclude_list = base_excluded_columns(Item)
    form_excluded_columns = base_form_excluded_columns(Item)
    column_type_formatters = custom_base_formatters
    details_template = "details_custom.html"
    column_formatters_detail = _column_formatters  # type: ignore
    column_formatters = _column_formatters  # type: ignore


class EquippedItemAdmin(ModelView, model=EquippedItem):
    column_list = [
        EquippedItem.id,
        EquippedItem.owner,
        EquippedItem.item,
        EquippedItem.amount,
        EquippedItem.equipped,
    ]
    column_details_exclude_list = base_excluded_columns(EquippedItem)
    form_excluded_columns = base_form_excluded_columns(EquippedItem)


class KnownSpellAdmin(ModelView, model=KnownSpell):
    column_list = [
        KnownSpell.id,
        KnownSpell.caster,
        KnownSpell.spell,
        KnownSpell.prepared,
    ]


class SpellAdmin(CustomModelView, model=Spell):
    _column_formatters = {
        Spell.school: lambda model, _: model.school.capitalize(),  # type: ignore
        "five_e_tools_url": lambda model, _: link(model.five_e_tools_url),
    }
    column_labels = {"five_e_tools_url": "5e.tools URL"}

    page_size = 30
    column_searchable_list = [Spell.name, Spell.level]
    column_list = [Spell.id, Spell.name, Spell.level, Spell.school]
    column_details_exclude_list = base_excluded_columns(Spell)
    form_excluded_columns = base_form_excluded_columns(Spell)
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
    form_excluded_columns = base_form_excluded_columns(PlayerRole)


class CustomAdmin(Admin):
    @login_required
    async def index(self, _: Request) -> Response:
        """Redirect admin index page to the listing of the first model view"""
        return RedirectResponse(url=f"{self.views[0].identity}/list")


def register_admin(app: FastAPI, engine: AsyncEngine) -> Admin:
    admin = CustomAdmin(app, engine, title="5esheets admin", templates_dir=str(templates_dir))
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
