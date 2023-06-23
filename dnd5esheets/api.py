from fastapi import APIRouter, Depends
from fastapi.routing import APIRoute
from sqlalchemy.ext.asyncio import AsyncSession

from .db import create_scoped_session
from .repositories import CharacterRepository
from .schemas import CharacterSchema, ListCharacterSchema, UpdateCharacterSchema


# https://fastapi.tiangolo.com/advanced/generate-clients/#custom-operation-ids-and-better-method-names
def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


api = APIRouter(prefix="/api", generate_unique_id_function=custom_generate_unique_id)


@api.get("/characters/", response_model=list[ListCharacterSchema], tags=["character"])
async def list_characters(
    session: AsyncSession = Depends(create_scoped_session),
):
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return await CharacterRepository.list_all(session)


@api.get("/characters/{slug}", response_model=CharacterSchema, tags=["character"])
async def display_character(
    slug: str, session: AsyncSession = Depends(create_scoped_session)
):
    """Display all details of a given character."""
    return await CharacterRepository.get_by_slug(session, slug=slug)


@api.put("/characters/{slug}", tags=["character"])
async def update_character(
    slug: str,
    character_data: UpdateCharacterSchema,
    session: AsyncSession = Depends(create_scoped_session),
) -> dict:
    """Update a character details.

    Examples of JSON body paylods:

    - `{"level": 5 }`
    - `{"name": "Toto"}`
    - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`

    In the last example, we update both a direct character attribute
    as well as an attribute nested in the character JSON data.

    """
    await CharacterRepository.update_character(session, slug, character_data)
    return {"status": "ok"}
