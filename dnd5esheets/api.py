from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession

from .db import create_scoped_session

from .schemas import ListCharacterSchema, CharacterSchema, UpdateCharacterSchema
from .repositories import CharacterRepository

api = APIRouter(prefix="/api")


@api.get("/characters/", response_model=list[ListCharacterSchema])
async def list_characters(
    session: AsyncSession = Depends(create_scoped_session),
):
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return await CharacterRepository.list_all(session)


@api.get("/characters/{slug}", response_model=CharacterSchema)
async def display_character(
    slug: str, session: AsyncSession = Depends(create_scoped_session)
):
    """Display all details of a given character."""
    return await CharacterRepository.get_by_slug(session, slug=slug)


@api.put("/characters/{slug}")
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
