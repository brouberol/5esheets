from fastapi import APIRouter
from fastapi.routing import APIRoute

from dnd5esheets.api.character import character_api
from dnd5esheets.api.party import party_api
from dnd5esheets.api.player import player_api


# https://fastapi.tiangolo.com/advanced/generate-clients/#custom-operation-ids-and-better-method-names
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


api = APIRouter(prefix="/api", generate_unique_id_function=custom_generate_unique_id)
api.include_router(character_api)
api.include_router(player_api)
api.include_router(party_api)
