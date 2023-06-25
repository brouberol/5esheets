from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from dnd5esheets.config import get_settings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.models import Player
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.schemas import JsonWebTokenData


class OptionalOAuth2PasswordBearer(OAuth2PasswordBearer):
    """Enable"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_error = get_settings().MULTITENANT_ENABLED


oauth2_scheme = OptionalOAuth2PasswordBearer(tokenUrl="token")


async def get_current_user_id(
    session: AsyncSession = Depends(create_scoped_session),
    settings=Depends(get_settings),
    token=Depends(oauth2_scheme),
) -> int | None:
    if not settings.MULTITENANT_ENABLED:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.JWT_ENCODING_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = JsonWebTokenData(username=username)
    except JWTError:
        raise credentials_exception
    player = await PlayerRepository.get_by_email(session, email=token_data.username)
    if player is None:
        raise credentials_exception
    return player.id
