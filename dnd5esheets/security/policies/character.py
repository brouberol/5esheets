"""Security policies related to Character resources"""

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.config.base import CommonSettings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.character import CharacterRepository
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.policies.base import _in_same_party, _is_party_gm
from dnd5esheets.security.user import get_current_user_id


async def party_gm_or_owner(
    request: Request,
    current_user_id=Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
    settings: CommonSettings = Depends(get_settings),
):
    """Security policy allowing access to a route only by the resource owner or the party GM"""
    if not settings.MULTITENANCY_ENABLED:
        return

    character_slug = request.scope["path_params"]["slug"]
    character = await CharacterRepository.get_by_slug(session, slug=character_slug)
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    if current_player == character.player:
        return
    return _is_party_gm(players=[current_player], party=character.party)


async def in_same_party(
    request: Request,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
    settings: CommonSettings = Depends(get_settings),
):
    """Security policy allowing access to a route only to players belonging to the same party"""
    if not settings.MULTITENANCY_ENABLED:
        return

    character_slug = request.scope["path_params"]["slug"]
    character = await CharacterRepository.get_by_slug(session, slug=character_slug)
    if character is None:
        return
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    players_in_party = (
        await PlayerRepository.get_all_players_with_characters_in_same_party_than_character(  # noqa
            session, character_slug=character_slug
        )
    )
    return _in_same_party(current_player=current_player, players_in_party=players_in_party)
