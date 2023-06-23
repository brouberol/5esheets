from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from sqlalchemy.ext.asyncio import AsyncSession

from .db import create_scoped_session

from .schemas import ListCharacterSchema, CharacterSchema, UpdateCharacterSchema
from .repositories import CharacterRepository, ModelNotFound

app = FastAPI()


@app.exception_handler(ModelNotFound)
def raise_404_exception_on_model_not_found(_: Request, exc: Exception):
    """Return a 404 response when handling a ModelNotFound exception"""
    return JSONResponse(content={"detail": str(exc)}, status_code=404)


@app.get("/characters/")
async def list_characters(
    session: AsyncSession = Depends(create_scoped_session),
) -> list[ListCharacterSchema]:
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return await CharacterRepository.list_all(session)


@app.get("/characters/{slug}")
async def display_character(
    slug: str, session: AsyncSession = Depends(create_scoped_session)
) -> CharacterSchema:
    """Display all details of a given character."""
    return await CharacterRepository.get_by_slug(session, slug=slug)


@app.put("/characters/{slug}")
async def update_character(
    slug: str,
    character_data: UpdateCharacterSchema,
    session: AsyncSession = Depends(create_scoped_session),
) -> dict:
    """Update a character details.

    Examples of JSON body paylods:

    - `{"level": 5 }`
    - `{"name": "Toto"}`
    - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`

    In the last example, we update both a direct character attribute
    as well as an attribute nested in the character JSON data.

    """
    await CharacterRepository.update_character(session, slug, character_data)
    return {"status": "ok"}
