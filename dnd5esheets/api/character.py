from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.character import CharacterRepository
from dnd5esheets.schemas import (
    CharacterSchema,
    CreateCharacterSchema,
    ListCharacterSchema,
    UpdateCharacterSchema,
)
from dnd5esheets.security.user import get_current_user_id

character_api = APIRouter(prefix="/character", tags=["character"])


@character_api.get("/", response_model=list[ListCharacterSchema])
async def list_characters(
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return await CharacterRepository.list_all(session, owner_id=current_player_id)


@character_api.get("/{slug}", response_model=CharacterSchema)
async def display_character(
    slug: str,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """Display all details of a given character."""
    return await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )


@character_api.put("/{slug}")
async def update_character(
    slug: str,
    character_data: UpdateCharacterSchema,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
) -> dict:
    """Update a character details.

    Examples of JSON body paylods:

    - `{"level": 5 }`
    - `{"name": "Toto"}`
    - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`

    In the last example, we update both a direct character attribute
    as well as an attribute nested in the character JSON data.

    """
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.update(session, slug, character_data)
    return {"status": "ok"}


@character_api.post("/new", response_model=CharacterSchema)
async def create_character(
    character_data: CreateCharacterSchema,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """Create a new character, without any data nor equipment"""
    return await CharacterRepository.create(
        session, character_data=character_data, owner_id=current_player_id
    )
