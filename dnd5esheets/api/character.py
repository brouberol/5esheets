from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from dnd5esheets.db import create_scoped_session
from dnd5esheets.etag import handle_etag_for_request
from dnd5esheets.repositories.character import CharacterRepository
from dnd5esheets.schemas import (
    CharacterSchema,
    CreateCharacterSchema,
    ListCharacterSchema,
    UpdateCharacterSchema,
)
from dnd5esheets.security.user import get_current_user_id

character_api = APIRouter(prefix="/character", tags=["character"])


async def handle_character_etag(
    session: AsyncSession,
    slug: str,
    owner_id: int | None,
    request: Request,
    response: Response,
):
    """Compute the character's etag, and handle any cache it"""
    etag = await CharacterRepository.etag(session, slug=slug, owner_id=owner_id)
    if etag is not None:
        handle_etag_for_request(etag, request, response)


@character_api.get(
    "/",
    response_model=list[ListCharacterSchema],
)
async def list_characters(
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return await CharacterRepository.list_all(session, owner_id=current_player_id)


@character_api.get(
    "/{slug}",
    response_model=CharacterSchema,
)
async def get_character(
    slug: str,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """Returns all details of a given character."""
    await handle_character_etag(session, slug, current_player_id, request, response)
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


@character_api.delete("/{slug}")
async def delete_character(
    slug: str,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """Delete the character associated with the slug and the currently logged in player id"""
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.delete(session, slug=slug, owner_id=current_player_id)
    return Response(status_code=HTTP_204_NO_CONTENT)


@character_api.put("/{slug}/equipment/{equipped_item_id}/equip")
async def equip_item(
    slug: str,
    equipped_item_id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
) -> dict:
    """Set the argument equipped item as equipped"""
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.change_equipment_item_equipped_status(
        session,
        slug=slug,
        owner_id=current_player_id,
        equipped_item_id=equipped_item_id,
        equipped=True,
    )
    return {"status": "ok"}


@character_api.put("/{slug}/equipment/{equipped_item_id}/unequip")
async def unequip_item(
    slug: str,
    equipped_item_id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
) -> dict:
    """Set the argument equipped item as unequipped"""
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.change_equipment_item_equipped_status(
        session,
        slug=slug,
        owner_id=current_player_id,
        equipped_item_id=equipped_item_id,
        equipped=False,
    )
    return {"status": "ok"}


@character_api.put("/{slug}/spellbook/{known_spell_id}/prepare")
async def prepare_spell(
    slug: str,
    known_spell_id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
) -> dict:
    """Set the argument known spell as prepared"""
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.change_known_spell_prepared_status(
        session,
        slug=slug,
        owner_id=current_player_id,
        known_spell_id=known_spell_id,
        prepared=True,
    )
    return {"status": "ok"}


@character_api.put("/{slug}/spellbook/{known_spell_id}/unprepare")
async def unprepare_spell(
    slug: str,
    known_spell_id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
) -> dict:
    """Set the argument known spell as unprepared"""
    await CharacterRepository.get_by_slug_if_owned(
        session, slug=slug, owner_id=current_player_id
    )
    await CharacterRepository.change_known_spell_prepared_status(
        session,
        slug=slug,
        owner_id=current_player_id,
        known_spell_id=known_spell_id,
        prepared=False,
    )
    return {"status": "ok"}
