"""
Definition of the pydandic models used for type validation and output serialization.
"""

from pydantic import BaseModel as BaseSchema, constr, Field


class BaseORMSchema(BaseSchema):
    class Config:
        orm_mode = True


class PlayerSchema(BaseORMSchema):
    id: int = Field(gt=0)
    name: constr(max_length=255)


class PartySchema(BaseORMSchema):
    id: int = Field(gt=0)
    name: constr(max_length=255)


class CharacterSchema(BaseORMSchema):
    id: int = Field(gt=0)
    name: constr(max_length=255)
    slug: constr(max_length=255)
    class_: constr(max_length=80)
    level: int = Field(gt=0)
    data: dict
    player: PlayerSchema
    party: PartySchema


class ListCharacterSchema(BaseORMSchema):
    id: int = Field(gt=0)
    name: constr(max_length=255)
    slug: constr(max_length=255)
    class_: constr(max_length=80)
    level: int = Field(gt=0)
    player: PlayerSchema
    party: PartySchema


class UpdateCharacterSchema(BaseSchema):
    name: constr(max_length=255) | None
    class_: constr(max_length=80) | None
    level: int | None = Field(gt=0)
    data: dict | None
