from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.schemas import DisplayPlayerSchema, UpdatePlayerSchema

player_api = APIRouter(prefix="/player", tags=["player"])


@player_api.get("/{id}", response_model=DisplayPlayerSchema)
async def display_player(
    id: int, session: AsyncSession = Depends(create_scoped_session)
):
    """Display all details of a given player."""
    return await PlayerRepository.get_by_id(session, id=id)


@player_api.put("/{id}")
async def update_player(
    id: int,
    player_data: UpdatePlayerSchema,
    session: AsyncSession = Depends(create_scoped_session),
) -> dict:
    """Update a player details.

    Examples of JSON body paylods:


    """
    await PlayerRepository.update(session, id, player_data)
    return {"status": "ok"}
