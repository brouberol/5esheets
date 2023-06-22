from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from .db import create_scoped_session

from .schemas import ListCharacterSchema, CharacterSchema, UpdateCharacterSchema
from .repositories import CharacterRepository

app = FastAPI()


@app.get("/characters/")
def list_characters(
    session: Session = Depends(create_scoped_session),
) -> list[ListCharacterSchema]:
    """List all characters.

    The returned payload will not include the character sheet details.

    """
    return CharacterRepository.list_all(session)


@app.get("/characters/{slug}")
def display_character(
    slug: str, session: Session = Depends(create_scoped_session)
) -> CharacterSchema:
    """Display all details of a given character."""
    character = CharacterRepository.get_by_slug(session, slug=slug)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@app.put("/characters/{slug}")
def update_character(
    slug: str,
    character_data: UpdateCharacterSchema,
    session: Session = Depends(create_scoped_session),
) -> dict:
    """Update a character details.

    Examples of JSON body paylods:

    - `{"level": 5 }`
    - `{"name": "Toto"}`
    - `{"class_": "Guerrier", "data": {"background": "Folk Hero"}}`

    In the last example, we update both a direct character attribute
    as well as an attribute nested in the character JSON data.

    """
    character = CharacterRepository.update_character(session, slug, character_data)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"status": "ok"}
