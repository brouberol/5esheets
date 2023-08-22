from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.exceptions import Forbidden
from dnd5esheets.models import Role
from dnd5esheets.repositories.character import CharacterRepository
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.user import get_current_user_id


async def party_gm_or_owner(
    request: Request,
    current_user_id=Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
):
    """Security policy allowing access to a route only by the resource owner or the associated party GM"""
    character_slug = request.scope["path_params"]["slug"]
    character = await CharacterRepository.get_by_slug(session, slug=character_slug)
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    if current_player == character.player:
        return
    character_party = character.party
    for player_role in current_player.player_roles:
        if player_role.party_id == character_party.id and player_role.role == Role.gm:
            return
    raise Forbidden(
        detail="Only the resource owner or the party GM can access this resource"
    )


async def in_same_party(
    request: Request,
    current_user_id: int | None = Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
):
    """Security policy allowing access to a route only to players belonging to the same party"""
    character_slug = request.scope["path_params"]["slug"]
    character = await CharacterRepository.get_by_slug(session, slug=character_slug)
    if character is None:
        return
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    players_in_party = await PlayerRepository.get_all_players_with_characters_in_same_party_than_character(
        session, character_slug=character_slug
    )
    if current_player not in players_in_party:
        raise Forbidden(
            detail="Only a member of the same party can access this resource"
        )
