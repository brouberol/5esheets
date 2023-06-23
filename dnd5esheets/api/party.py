from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.schemas import DisplayPartySchema, UpdatePartySchema

party_api = APIRouter(prefix="/party", tags=["player"])


@party_api.get("/{id}", response_model=DisplayPartySchema)
async def display_party(
    id: int, session: AsyncSession = Depends(create_scoped_session)
):
    """Display all details of a given party."""
    return await PartyRepository.get_by_id(session, id=id)


@party_api.put("/{id}")
async def update_party(
    id: int,
    player_data: UpdatePartySchema,
    session: AsyncSession = Depends(create_scoped_session),
) -> dict:
    """Update a party details.

    Examples of JSON body paylods:


    """
    await PartyRepository.update(session, id, player_data)
    return {"status": "ok"}
