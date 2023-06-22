from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from .db import create_scoped_session

from .schemas import ListCharacterSchema, CharacterSchema, UpdateCharacterSchema
from .repositories import CharacterRepository

app = FastAPI()


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
    character = await CharacterRepository.get_by_slug(session, slug=slug)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


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
    character = await CharacterRepository.update_character(
        session, slug, character_data
    )
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"status": "ok"}
