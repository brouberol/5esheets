from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.exceptions import ModelNotFound
from dnd5esheets.models import Player
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.security.hashing import verify_password
from dnd5esheets.security.user import access_security

login_api = APIRouter(prefix="/login", tags=["login"])


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
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(create_scoped_session),
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
    subject = {"username": player.email}
    access_token = access_security.create_access_token(
        subject=subject,
    )
    access_security.set_access_cookie(response, access_token=access_token)
    return {"status": "logged_in"}
