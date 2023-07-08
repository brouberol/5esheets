"""
Definition of the pydandic models used for type validation and output serialization.
"""

from enum import Enum

from pydantic import BaseModel as BaseSchema
from pydantic import Field


class Proficiency(Enum):
    none: int = 0
    proficient: int = 1
    master: int = 2


class ActionType(Enum):
    action: str = "action"
    bonus: str = "bonus_action"
    reaction: str = "reaction"


class SpellOrigin(Enum):
    subclass: str = "class"


class BaseUpdateSchema(BaseSchema, extra="forbid"):
    ...


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


class PlayerSchema(BaseORMSchema):
    """The basic details of a player"""

    id: int = Field(ge=1, title="The player primary key in database")
    name: str = Field(max_length=255, title="The player name")


class DisplayPlayerSchema(PlayerSchema):
    """A player details including the list of their characters"""

    characters: list["CharacterSchemaNoPlayer"] = Field(title="The player's characters")


class UpdatePlayerSchema(BaseUpdateSchema):
    name: str | None = Field(max_length=255, title="The player new name")


class PartySchema(BaseORMSchema):
    """The basic details of a party"""

    id: int = Field(ge=1, title="The party primary key in database")
    name: str = Field(max_length=255, title="The party name")


class DisplayPartySchema(PartySchema):
    """A party details, including the members"""

    members: list["CharacterSchemaNoPartyNoData"] = Field(title="The party members")


class UpdatePartySchema(BaseUpdateSchema):
    name: str | None = Field(max_length=255, title="The party new name")


class SaveProficiencies(BaseSchema):
    strength: Proficiency
    dexterity: Proficiency
    constitution: Proficiency
    intelligence: Proficiency
    charisma: Proficiency
    wisdom: Proficiency


class SkillProficiencies(BaseSchema):
    acrobatics: Proficiency
    arcana: Proficiency
    athletics: Proficiency
    stealth: Proficiency
    animal_handling: Proficiency
    sleight_of_hand: Proficiency
    history: Proficiency
    intimidation: Proficiency
    investigation: Proficiency
    medicine: Proficiency
    nature: Proficiency
    perception: Proficiency
    insight: Proficiency
    persuasion: Proficiency
    religion: Proficiency
    performance: Proficiency
    survival: Proficiency
    deception: Proficiency


class Proficiencies(BaseSchema):
    saves: SaveProficiencies
    skills: SkillProficiencies


class Scores(BaseSchema):
    strength: int
    dexterity: int
    constitution: int
    wisdom: int
    charisma: int
    intelligence: int


class HitPoints(BaseSchema):
    max: int
    temp: int
    current: int


class HitDice(BaseSchema):
    type: str
    total: int
    remaining: int


class CustomResource(BaseSchema):
    header: str
    available: int
    remaining: int


class Attack(BaseSchema):
    name: str
    bonus: int
    damage: str
    damage_type: str


class Money(BaseSchema):
    copper: int
    silver: int
    electrum: int
    gold: int
    platinum: int


class Spell(BaseSchema):
    name: str
    description: str
    prepared: bool = False
    somatic: bool = False
    verbal: bool = False
    material: bool = False
    ritual: bool = False
    concentration: bool = False
    invocation: ActionType | None = None
    origin: SpellOrigin | None = None


class Spells(BaseSchema):
    spellcasting_ability: str
    daily_prepared: int
    cantrips: list[Spell] = []
    lvl1: list[Spell] = []
    lvl2: list[Spell] = []
    lvl3: list[Spell] = []
    lvl4: list[Spell] = []
    lvl5: list[Spell] = []
    lvl6: list[Spell] = []
    lvl7: list[Spell] = []
    lvl8: list[Spell] = []
    lvl9: list[Spell] = []


class CharacterSheet(BaseSchema):
    scores: Scores
    proficiencies: Proficiencies
    xp: int
    race: str
    background: str
    alignment: str
    darkvision: bool
    inspiration: bool
    speed: int
    hp: HitPoints
    hit_dice: HitDice
    custom_resources: list[CustomResource]
    attacks: list[Attack]
    equipment: str
    languages_and_proficiencies: str
    personality: str
    ideals: str
    bonds: str
    features: str
    spells: Spells


class CharacterSchema(BaseORMSchema):
    """All details associated with a character"""

    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(
        max_length=255, title="The character slug, used to identify it in the API"
    )
    class_: str = Field(max_length=80, title="The character class")
    level: int = Field(ge=1, title="The character level")
    data: CharacterSheet = Field(description="The embdedded character sheet JSON data")
    party: PartySchema = Field(title="The embedded character's party schema")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    equipment: list[EquippedItemSchema] = Field(title="The character's equipment")


class CharacterSchemaNoPlayer(CharacterSchema):
    """The details of a character, excluding the player"""

    player: PlayerSchema = Field(exclude=True)
    data: dict = Field(exclude=True)  # type: ignore


class CharacterSchemaNoPartyNoData(CharacterSchema):
    """The details of a character, excluding the party"""

    party: PartySchema = Field(exclude=True)
    data: dict = Field(exclude=True)  # type: ignore


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


class UpdateCharacterSchema(BaseUpdateSchema):
    name: str | None = Field(title="A new character name (Optional)")
    class_: str | None = Field(max_length=80, title="A new character class (Optional)")
    level: int | None = Field(ge=1, title="A new character level (Optional)")
    data: dict | None = Field(title="Updates to the character sheet fields (Optional)")


DisplayPlayerSchema.update_forward_refs()
DisplayPartySchema.update_forward_refs()
