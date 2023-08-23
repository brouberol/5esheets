from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.schemas import DisplayPartySchema, PartySchema, UpdatePartySchema
from dnd5esheets.security.policies.party import in_same_party, is_party_gm
from dnd5esheets.security.user import get_current_user_id

party_api = APIRouter(prefix="/party", tags=["party"])


@party_api.get("/", response_model=list[PartySchema])
async def list_all_parties(
    session: AsyncSession = Depends(create_scoped_session),
    current_player_id: int | None = Depends(get_current_user_id),
):
    """List all parties the current player has characters in"""
    return await PartyRepository.list_all(session=session, owner_id=current_player_id)


@party_api.get(
    "/{id}", dependencies=[Depends(in_same_party)], response_model=DisplayPartySchema
)
async def display_party(
    id: int,
    session: AsyncSession = Depends(create_scoped_session),
):
    """Display details of a given party"""
    return await PartyRepository.get_by_id(session=session, id=id)


@party_api.put("/{id}", dependencies=[Depends(is_party_gm)])
async def update_party(
    id: int,
    party_data: UpdatePartySchema,
    session: AsyncSession = Depends(create_scoped_session),
) -> dict:
    """Update a party details.

    Examples of JSON body paylods:


    """
    await PartyRepository.update(
        session=session,
        id=id,
        body=party_data,
    )
    return {"status": "ok"}
