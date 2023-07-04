from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.schemas import JsonWebTokenData


async def get_current_user_id(
    request: Request,
    session: AsyncSession = Depends(create_scoped_session),
    settings=Depends(get_settings),
    Authorize: AuthJWT = Depends(),
) -> int | None:
    if not settings.MULTITENANT_ENABLED:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    Authorize._verify_and_get_jwt_optional_in_cookies(request)
    try:
        username: str | None = Authorize.get_jwt_subject()
        if not username:
            raise credentials_exception
        token_data = JsonWebTokenData(username=username)
    except AuthJWTException:
        raise credentials_exception
    player = await PlayerRepository.get_by_email(session, email=token_data.username)
    if player is None:
        raise credentials_exception
    return player.id
