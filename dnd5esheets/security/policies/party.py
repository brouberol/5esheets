"""Security policies related to Party resources"""

from typing import cast

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.config.base import CommonSettings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.models import Party
from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.policies.base import _in_same_party, _is_party_gm
from dnd5esheets.security.user import get_current_user_id


async def is_party_gm(
    request: Request,
    current_user_id=Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
    settings: CommonSettings = Depends(get_settings),
):
    """Security policy allowing access to a route only by the resource owner or the party GM"""
    if not settings.MULTITENANT_ENABLED:
        return

    party_id = request.scope["path_params"]["id"]
    party = cast(Party, await PartyRepository.get_by_id(session, id=party_id))
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    players_in_party = await PlayerRepository.get_all_players_with_characters_in_party(
        session, party_id=party_id, player_id=current_player.id
    )
    return _is_party_gm(players=players_in_party, party=party)


async def in_same_party(
    request: Request,
    current_user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
    settings: CommonSettings = Depends(get_settings),
):
    """Security policy allowing access to a route only to players belonging to the same party"""
    if not settings.MULTITENANT_ENABLED:
        return

    party_id = request.scope["path_params"]["id"]
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    players_in_party = await PlayerRepository.get_all_players_with_characters_in_party(
        session, party_id=party_id
    )
    return _in_same_party(
        current_player=current_player, players_in_party=players_in_party
    )
