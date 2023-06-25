from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.models import Player
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.schemas import DisplayPlayerSchema, UpdatePlayerSchema
from dnd5esheets.security.user import get_current_user

player_api = APIRouter(prefix="/player", tags=["player"])


@player_api.get("/{id}", response_model=DisplayPlayerSchema)
async def display_player(
    id: int,
    session: AsyncSession = Depends(create_scoped_session),
    current_player: Player = Depends(get_current_user),
):
    """Display all details of a given player."""
    if id != current_player.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return await PlayerRepository.get_by_id(session, id=id)


@player_api.put("/{id}")
async def update_player(
    id: int,
    player_data: UpdatePlayerSchema,
    session: AsyncSession = Depends(create_scoped_session),
    current_player: Player = Depends(get_current_user),
) -> dict:
    """Update a player details.

    Examples of JSON body paylods:


    """
    if id != current_player.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await PlayerRepository.update(session, id, player_data)
    return {"status": "ok"}
