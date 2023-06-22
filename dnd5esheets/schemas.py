"""
Definition of the pydandic models used for type validation and output serialization.
"""

from pydantic import BaseModel as BaseSchema, constr, Field


class BaseORMSchema(BaseSchema):
    class Config:
        orm_mode = True


class PlayerSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The player primary key in database")
    name: str = Field(max_length=255, title="The player name")


class PartySchema(BaseORMSchema):
    id: int = Field(ge=1, title="The party primary key in database")
    name: str = Field(max_length=255, title="The party name")


class CharacterSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(
        max_length=255, title="The character slug, used to identify it in the API"
    )
    class_: str = Field(max_length=80, title="The character class")
    level: int = Field(ge=1, title="The character level")
    data: dict = Field(description="The embdedded character sheet JSON data")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    party: PartySchema = Field(title="The embedded character's party schema")


class ListCharacterSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(
        max_length=255, title="The character slug, used to identify it in the API"
    )
    class_: str = Field(max_length=80, title="The character class")
    level: int = Field(ge=1, le=20, title="The character level")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    party: PartySchema = Field(title="The embedded character's party schema")


class UpdateCharacterSchema(BaseSchema):
    name: str | None = Field(title="A new character name (Optional)")
    class_: str | None = Field(max_length=80, title="A new character class (Optional)")
    level: int | None = Field(ge=1, title="A new character level (Optional)")
    data: dict | None = Field(title="Updates to the character sheet fields (Optional)")
