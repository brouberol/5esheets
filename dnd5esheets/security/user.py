from fastapi import Depends, HTTPException, status, Security
from fastapi_jwt import (
    JwtAuthorizationCredentials,
    JwtAccessBearerCookie,
)
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.player import PlayerRepository

access_security = JwtAccessBearerCookie(
    secret_key=get_settings().AUTHJWT_SECRET_KEY,
    auto_error=False,
    access_expires_delta=get_settings().AUTHJWT_ACCESS_TOKEN_EXPIRES,
)


async def get_current_user_id(
    session: AsyncSession = Depends(create_scoped_session),
    settings=Depends(get_settings),
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> int | None:
    if not settings.MULTITENANT_ENABLED:
        return None
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not credentials:
        raise credentials_exception

    player = await PlayerRepository.get_by_email(
        session, email=credentials.subject["username"]
    )
    if player is None:
        raise credentials_exception

    return player.id
