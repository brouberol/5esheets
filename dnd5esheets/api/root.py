from fastapi import APIRouter
from fastapi.routing import APIRoute

from dnd5esheets.api.character import character_api


# https://fastapi.tiangolo.com/advanced/generate-clients/#custom-operation-ids-and-better-method-names
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


api = APIRouter(prefix="/api", generate_unique_id_function=custom_generate_unique_id)
api.include_router(character_api)
