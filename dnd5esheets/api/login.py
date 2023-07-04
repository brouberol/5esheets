from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.config import get_settings
from dnd5esheets.db import create_scoped_session
from dnd5esheets.models import Player
from dnd5esheets.repositories import ModelNotFound
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.hashing import verify_password

login_api = APIRouter(prefix="/login", tags=["login"])


@AuthJWT.load_config
def get_config():
    """Configure the JWT authentication mechanism from the application configuration"""
    return get_settings()


async def authenticate_player(
    username: str, password: str, session: AsyncSession
) -> tuple[bool, Optional[Player]]:
    try:
        player = await PlayerRepository.get_by_email(email=username, session=session)
    except ModelNotFound:
        return False, None
    if not verify_password(password, player.hashed_password):
        return False, None
    return True, player


@login_api.post("/token")
async def login_for_access_token(
    _: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(create_scoped_session),
    Authorize: AuthJWT = Depends(),
):
    """Submit a player's username and password to login.

    If the password verifies, returns a JWT usable to communicate with the API.
    If not, raise a 401 error.

    """
    authenticated, player = await authenticate_player(
        username=form_data.username, password=form_data.password, session=session
    )
    if not (authenticated and player):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = Authorize.create_access_token(
        subject=player.email,
    )
    Authorize.set_access_cookies(access_token)
    return {"status": "logged_in"}
