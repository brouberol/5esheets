from fastapi import APIRouter
from fastapi.routing import APIRoute

from dnd5esheets import ExtendedFastAPI
from dnd5esheets.api.character import character_api
from dnd5esheets.api.debug import debug_api
from dnd5esheets.api.item import item_api
from dnd5esheets.api.login import login_api
from dnd5esheets.api.party import party_api
from dnd5esheets.api.player import player_api
from dnd5esheets.api.spell import spell_api
from dnd5esheets.config import Env, get_env


# https://fastapi.tiangolo.com/advanced/generate-clients/#custom-operation-ids-and-better-method-names
def custom_generate_unique_id(route: APIRoute):
    if route.tags:
        return f"{route.tags[0]}-{route.name}"
    return route.name


def register_api(app: ExtendedFastAPI):
    api = APIRouter(prefix="/api", generate_unique_id_function=custom_generate_unique_id)
    api.include_router(character_api)
    api.include_router(party_api)
    api.include_router(player_api)
    api.include_router(login_api)
    api.include_router(spell_api)
    api.include_router(item_api)
    if get_env() != Env.prod:
        api.include_router(debug_api)
    app.include_router(api)
