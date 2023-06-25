from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.models import Player
from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.schemas import DisplayPartySchema, PartySchema, UpdatePartySchema
from dnd5esheets.security.user import get_current_user

party_api = APIRouter(prefix="/party", tags=["party"])


@party_api.get("/", response_model=list[PartySchema])
async def list_all_parties(
    session: AsyncSession = Depends(create_scoped_session),
    current_player: Player = Depends(get_current_user),
):
    """List all parties the current player has characters in"""
    return await PartyRepository.list_all(session=session, owner_id=current_player.id)


@party_api.get("/{id}", response_model=DisplayPartySchema)
async def display_party(
    id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player: Player = Depends(get_current_user),
):
    """Display all details of a given party."""
    return await PartyRepository.get_by_id_if_member_of(
        session=session, id=id, member_id=current_player.id
    )


@party_api.put("/{id}")
async def update_party(
    id: int,
    player_data: UpdatePartySchema,
    session: AsyncSession = Depends(create_scoped_session),
    current_player: Player = Depends(get_current_user),
) -> dict:
    """Update a party details.

    Examples of JSON body paylods:


    """
    await PartyRepository.update_if_member_of(
        session=session, id=id, body=player_data, member_id=current_player.id
    )
    return {"status": "ok"}
