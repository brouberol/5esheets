"""
Definition of the pydandic models used for type validation and output serialization.
"""

from pydantic import BaseModel as BaseSchema
from pydantic import Field


class JsonWebToken(BaseSchema):
    access_token: str
    token_type: str


class JsonWebTokenData(BaseSchema):
    username: str


class BaseORMSchema(BaseSchema):
    class Config:
        orm_mode = True


class ItemSchema(BaseORMSchema):
    """The details of an equipment item"""

    name: str = Field(max_length=255, title="The item name")
    data: dict = Field(description="The embdedded item JSON data")


class EquippedItemSchema(BaseORMSchema):
    """The details of an equipped item (the association bewteen an item and a character equipment)"""

    item: ItemSchema = Field(title="The equipped item details")
    amount: int = Field(
        title="The amount of associated items found in the character's equipment"
    )
    equipped: bool = Field(title="Weather the item is currently equipped")


class EquipmentSchema(BaseORMSchema):
    """The details of a character's equipment"""

    items: list["EquippedItemSchema"]


class PlayerSchema(BaseORMSchema):
    """The basic details of a player"""

    id: int = Field(ge=1, title="The player primary key in database")
    name: str = Field(max_length=255, title="The player name")


class DisplayPlayerSchema(PlayerSchema):
    """A player details including the list of their characters"""

    characters: list["CharacterSchemaNoPlayer"] = Field(title="The player's characters")


class UpdatePlayerSchema(BaseSchema):
    name: str | None = Field(max_length=255, title="The player new name")


class PartySchema(BaseORMSchema):
    """The basic details of a party"""

    id: int = Field(ge=1, title="The party primary key in database")
    name: str = Field(max_length=255, title="The party name")


class DisplayPartySchema(PartySchema):
    """A party details, including the members"""

    members: list["CharacterSchemaNoPartyNoData"] = Field(title="The party members")


class UpdatePartySchema(BaseSchema):
    name: str | None = Field(max_length=255, title="The party new name")


class CharacterSchema(BaseORMSchema):
    """All details associated with a character"""

    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(
        max_length=255, title="The character slug, used to identify it in the API"
    )
    class_: str = Field(max_length=80, title="The character class")
    level: int = Field(ge=1, title="The character level")
    data: dict = Field(description="The embdedded character sheet JSON data")
    party: PartySchema = Field(title="The embedded character's party schema")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    equipment: EquipmentSchema = Field(title="The character's equipment")


class CharacterSchemaNoPlayer(CharacterSchema):
    """The details of a character, excluding the player"""

    player: PlayerSchema = Field(exclude=True)


class CharacterSchemaNoPartyNoData(CharacterSchema):
    """The details of a character, excluding the party"""

    party: PartySchema = Field(exclude=True)
    data: dict = Field(exclude=True)


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


DisplayPlayerSchema.update_forward_refs()
DisplayPartySchema.update_forward_refs()
