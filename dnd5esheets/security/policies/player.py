"""Security policies related to Party resources"""

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.config.base import CommonSettings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.exceptions import Forbidden
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.user import get_current_user_id


async def is_owner(
    request: Request,
    current_user_id=Depends(get_current_user_id),
    session: AsyncSession = Depends(create_scoped_session),
    settings: CommonSettings = Depends(get_settings),
):
    """Security policy allowing access to a route only by the resource owner"""
    if not settings.MULTITENANT_ENABLED:
        return

    player_id = request.scope["path_params"]["id"]
    player = await PlayerRepository.get_by_id(session, id=player_id)
    current_player = await PlayerRepository.get_by_id(session, current_user_id)
    if player != current_player:
        raise Forbidden(detail="This resource can only be accessed by its owner")
