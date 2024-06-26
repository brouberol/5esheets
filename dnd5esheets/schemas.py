"""
Definition of the pydandic models used for type validation and output serialization.
"""

from enum import IntEnum, StrEnum
from typing import Literal, Optional, cast

from pydantic import BaseModel as BaseSchema
from pydantic import ConfigDict, Field, computed_field

from dnd5esheets.models import Role


class BaseUpdateSchema(BaseSchema, extra="forbid"): ...


class BaseORMSchema(BaseSchema):
    model_config = ConfigDict(from_attributes=True)


# We define a special field to mark the fields with a default value of 0
# server-side, which _actual_ value will be computed by the frontend, based
# on other fields values (ex: proficiency bonus based on the level).
# We mark these fields with a special description value, because pydantic marks
# fields with a default value as optional, which gets generated into a
# <name>?: number; field when generating the typescript client.
# That is an issue, because the server sends a non-nil default value. We rely
# on that custom description to specify these fields as required in the openapi
# spec, to make sure these fields are marked as required in the TS client.
FrontendComputedField = Field(default=0, description="frontend_computed")


class AbilityName(StrEnum):
    charisma: str = "charisma"
    constitution: str = "constitution"
    dexterity: str = "dexterity"
    intelligence: str = "intelligence"
    strength: str = "strength"
    wisdom: str = "wisdom"


class Proficiency(IntEnum):
    none: int = 0
    proficient: int = 1
    master: int = 2


class ActionType(StrEnum):
    action: str = "action"
    bonus: str = "bonus_action"
    reaction: str = "reaction"


class MagicSchool(StrEnum):
    necromancy: str = "necromancy"
    evocation: str = "evocation"
    enchantment: str = "enchantment"
    illusion: str = "illusion"
    transmutation: str = "transmutation"
    abjuration: str = "abjuration"
    conjuration: str = "conjuration"
    divination: str = "divination"


class TimeUnit(StrEnum):
    action = "action"
    bonus = "bonus"
    reaction = "reaction"
    minute = "minute"
    hour = "hour"


class DurationUnit(StrEnum):
    day = "day"
    hour = "hour"
    minute = "minute"
    round = "round"


class WeaponCategory(StrEnum):
    simple = "simple"
    heavy = "heavy"


class WeaponType(StrEnum):
    axe = "axe"
    bow = "bow"
    club = "club"
    crossbow = "crossbow"
    dagger = "dagger"
    hammer = "hammer"
    mace = "mace"
    net = "net"
    spear = "spear"
    staff = "staff"
    sword = "sword"


class SpellCastingFocusType(StrEnum):
    arcane = "arcane"
    druid = "druid"


class SpellOrigin(StrEnum):
    subclass: str = "class"


class ResourceSource(BaseSchema):
    book: str = Field(title="The resource source book")
    page: int = Field(ge=0, title="The page the resource is described at")


class ResourceTranslation(BaseSchema):
    name: str = Field(title="The spell translated name")
    description: str = Field(title="The spell translated description")


class ItemAttributes(BaseSchema):
    weapon_category: WeaponCategory
    weapon_type: Optional[WeaponType] = Field(default=None)
    ammo_type: Optional[str] = Field(default=None)
    spellcasting_focus_type: Optional[SpellCastingFocusType] = Field(default=None)
    range: Optional[str] = Field(default=None)


class ItemDamage(BaseSchema):
    damage_1: str
    damage_type: str
    damage_2: Optional[str] = Field(default=None)


class ItemMeta(BaseSchema):
    translations: Optional[dict[str, ResourceTranslation]] = Field(default_factory=dict)
    rarity: str
    weight: Optional[float] = Field(default=None)
    value: float
    attributes: Optional[ItemAttributes] = Field(default=None)
    damage: Optional[ItemDamage] = Field(default=None)
    property: Optional[list[str]] = Field(default_factory=list)
    effect: Optional[str] = Field(default=None)
    requirements: Optional[dict] = Field(default_factory=dict)
    stealth: Optional[bool] = Field(default=None)


class ItemData(BaseSchema):
    source: ResourceSource
    srd: bool
    subtype: str
    meta: ItemMeta


class ItemSchema(BaseORMSchema):
    """The details of an equipment item"""

    name: str = Field(max_length=255, title="The item name")
    data: ItemData = Field(description="The embdedded item JSON data")


class EquippedItemSchema(BaseORMSchema):
    """The details of an equipped item (the association bewteen an item and a character equipment)"""

    id: int = Field(ge=1, title="The equipped item id in database")
    item: ItemSchema = Field(title="The equipped item details")
    amount: int = Field(
        title="The amount of associated items found in the character's equipment", ge=0
    )
    equipped: bool = Field(title="Whether the item is currently equipped")


class SpellCastingMaterial(BaseSchema):
    text: str = Field(title="A description of the material components required to cast a spell")
    cost: int = Field(title="The minimum cost of the materials", default=0)
    consume: bool | str = Field(default=None)


class SpellCasting(BaseSchema):
    verbal: Optional[bool] = Field(
        title="Whether casting the spell requires a vocal component", default=False
    )
    somatic: Optional[bool] = Field(
        title="Whether casting the spell requires a somatic component", default=False
    )
    material: Optional[SpellCastingMaterial] = Field(
        title="The material components required to cast the spell", default=None
    )
    concentration: Optional[bool] = Field(
        title="Whether casting the spell requires maintaining concentration",
        default=False,
    )
    ritual: Optional[bool] = Field(
        title="Whether the spell can be casted as a ritual",
        default=False,
    )


class ListingSpellCasting(SpellCasting):
    material: Optional[SpellCastingMaterial] = Field(exclude=True, default=None)

    @computed_field
    def needs_material(self) -> bool:
        """Whether the spell requires material components"""
        return bool(self.material)


class SpellTime(BaseSchema):
    number: int = Field(title="The amount of time units it takes to cast the spell")
    unit: TimeUnit = Field(title="The type of time unit it takes to cast the spell")
    condition: str | None = Field(
        title="A possible condition before being able to cast the spell", default=None
    )


class SpellRangeDistance(BaseSchema):
    type: str
    amount: Optional[int] = Field(default=None)


class SpellRange(BaseSchema):
    type: str
    distance: Optional[SpellRangeDistance] = Field(default=None)


class SpellDuration(BaseSchema):
    type: str
    unit: Optional[DurationUnit] = Field(default=None)
    amount: Optional[int] = Field(default=0)
    ends: Optional[list[str]] = Field(default_factory=list)


class SpellScalingLevel(BaseSchema):
    label: str
    scaling: dict[str, str]


class SpellMeta(BaseSchema):
    description: str = Field(title="The spell description")
    translations: dict[str, ResourceTranslation] = Field(
        title="Translations of the spell name and description", default_factory=dict
    )


class SpellData(BaseSchema):
    source: ResourceSource
    casting: SpellCasting
    meta: SpellMeta
    time: list[SpellTime]
    range: SpellRange
    duration: list[SpellDuration]
    misc_tags: list[str] = Field(default=[])
    area_tags: list[str] = Field(default=[])
    scaling_level_dice: list[SpellScalingLevel] = Field(default_factory=list)
    damage_inflict: list[str] = Field(default=[])
    saving_throw: list[str] = Field(default=[])
    condition_inflict: list[str] = Field(default=[])
    affects_creature_type: list[str] = Field(default=[])
    spell_attack: list[str] = Field(default=[])
    ability_check: list[AbilityName] = Field(default=[])
    damage_resist: list[str] = Field(default=[])
    condition_immune: list[str] = Field(default=[])
    damage_vulnerable: list[str] = Field(default=[])
    damage_immune: list[str] = Field(default=[])


class RestrictedSpellData(BaseSchema):
    casting: ListingSpellCasting


class SpellSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The spell primary key in database")
    name: str = Field(title="The spell name")
    level: int = Field(ge=0, le=9, title="The spell level")
    school: MagicSchool = Field(title="The spell magic school")
    data: SpellData


class RestrictedSpellSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The spell primary key in database")
    name: str = Field(title="The spell name")
    level: int = Field(ge=0, le=9, title="The spell level")
    school: MagicSchool = Field(title="The spell magic school")
    data: RestrictedSpellData


class RestrictedKnownSpellSchema(BaseORMSchema):
    """The details of a known spell (the association between a character and a spell)"""

    id: int = Field(ge=1, title="The known spell primary key in database")
    prepared: bool = Field(title="Whether the spell is currently prepared")
    spell: RestrictedSpellSchema = Field(title="The spell details")


class PlayerRole(BaseORMSchema):
    """The details of a player role"""

    role: Role
    party_id: int


class PlayerSchema(BaseORMSchema):
    """The basic details of a player"""

    id: int = Field(ge=1, title="The player primary key in database")
    name: str = Field(max_length=255, title="The player name")
    player_roles: list[PlayerRole]


class DisplayPlayerSchema(PlayerSchema):
    """A player details including the list of their characters"""

    characters: list["RestrictedCharacterSchema"] = Field(title="The player's characters")


class UpdatePlayerSchema(BaseUpdateSchema):
    name: str | None = Field(max_length=255, title="The player new name", default=None)


class PartySchema(BaseORMSchema):
    """The basic details of a party"""

    id: int = Field(ge=1, title="The party primary key in database")
    name: str = Field(max_length=255, title="The party name")


class DisplayPartySchema(PartySchema):
    """A party details, including the members"""

    members: list["CharacterSchemaNoEmbeddedFields"] = Field(title="The party members")


class UpdatePartySchema(BaseUpdateSchema):
    name: str | None = Field(max_length=255, title="The party new name", default=None)


class SaveProficiencies(BaseSchema):
    charisma: Proficiency = Proficiency.none
    constitution: Proficiency = Proficiency.none
    dexterity: Proficiency = Proficiency.none
    intelligence: Proficiency = Proficiency.none
    strength: Proficiency = Proficiency.none
    wisdom: Proficiency = Proficiency.none


class Ability(BaseSchema):
    score: int = Field(title="The ability score", ge=0, le=30, default=0)
    proficiency: Proficiency = Proficiency.none

    # Autocomputed fields, declared here to have them part of the TS types
    modifier: int = FrontendComputedField
    save: int = FrontendComputedField


class Abilities(BaseSchema):
    charisma: Ability = Ability()
    constitution: Ability = Ability()
    dexterity: Ability = Ability()
    intelligence: Ability = Ability()
    strength: Ability = Ability()
    wisdom: Ability = Ability()


class Skill(BaseSchema):
    # Autocomputed fields, declared here to have them part of the TS types
    proficiency: Proficiency = Proficiency.none
    modifier: int = FrontendComputedField


class Skills(BaseSchema):
    acrobatics: Skill = Skill()
    arcana: Skill = Skill()
    athletics: Skill = Skill()
    stealth: Skill = Skill()
    animal_handling: Skill = Skill()
    sleight_of_hand: Skill = Skill()
    history: Skill = Skill()
    intimidation: Skill = Skill()
    investigation: Skill = Skill()
    medicine: Skill = Skill()
    nature: Skill = Skill()
    perception: Skill = Skill()
    insight: Skill = Skill()
    persuasion: Skill = Skill()
    religion: Skill = Skill()
    performance: Skill = Skill()
    survival: Skill = Skill()
    deception: Skill = Skill()


class HitPoints(BaseSchema):
    max: int = Field(ge=0, default=0)
    temp: int = Field(ge=0, default=0)
    current: int = Field(ge=0, default=0)


class HitDice(BaseSchema):
    type: str = ""
    total: int = Field(ge=0, default=0)
    remaining: int = Field(ge=0, default=0)


class CustomResource(BaseSchema):
    header: str = ""
    available: int = Field(ge=0, default=0)
    remaining: int = Field(ge=0, default=0)


class Attack(BaseSchema):
    name: str
    bonus: int
    damage: str
    damage_type: str


class Money(BaseSchema):
    copper: int = Field(title="Amount of copper coins", ge=0, default=0)
    silver: int = Field(title="Amount of silver coins", ge=0, default=0)
    electrum: int = Field(title="Amount of electrum coins", ge=0, default=0)
    gold: int = Field(title="Amount of gold coins", ge=0, default=0)
    platinum: int = Field(title="Amount of platinum coins", ge=0, default=0)


class CharacterClass(BaseSchema):
    name: str
    variant: str | None
    level: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]


class CharacterSheet(BaseSchema):
    classes: list[CharacterClass] = []
    abilities: Abilities = Abilities()
    skills: Skills = Skills()
    xp: int = Field(ge=0, default=0)
    race: str = ""
    background: str = ""
    alignment: str = ""
    darkvision: bool = False
    inspiration: bool = False
    speed: int = Field(ge=0, default=30)
    hp: HitPoints = HitPoints()
    hit_dice: HitDice = HitDice()
    money: Money = Money()
    custom_resources: list[CustomResource] = []
    attacks: list[Attack] = []
    languages_and_proficiencies: str = ""
    personality: str = ""
    ideals: str = ""
    bonds: str = ""
    flaws: str = ""
    features: str = ""
    inventory: str = ""
    spellcasting_ability: AbilityName | None = None
    daily_prepared_spells: int = 0
    exhaustion: Literal[0, 1, 2, 3, 4, 5, 6] = 0

    # These are optional fields are they are calculated by the frontend.
    # We declare them here so that they appear in the generated TS types.
    proficiency_bonus: int = FrontendComputedField
    ac: int = FrontendComputedField
    initiative: int = FrontendComputedField
    spell_dc: int = FrontendComputedField
    spell_attack_bonus: int = FrontendComputedField
    passive_perception: int = FrontendComputedField

    @classmethod
    def new_empty(cls) -> "CharacterSheet":
        return cast(CharacterSheet, CharacterSheet.model_validate({}).model_dump())


class CharacterSchema(BaseORMSchema):
    """All details associated with a character"""

    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(max_length=255, title="The character slug, used to identify it in the API")
    level: int | None = Field(ge=0, le=20, title="The character level", default=None)
    data: CharacterSheet | None = Field(
        description="The embdedded character sheet JSON data", default=None
    )
    party: PartySchema = Field(title="The embedded character's party schema")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    equipment: list[EquippedItemSchema] = Field(title="The character's equipment")
    spellbook: list[RestrictedKnownSpellSchema] = Field(title="The character's spellbook content")


class CreateCharacterSchema(BaseORMSchema):
    """All details associated with a character"""

    name: str = Field(max_length=255, title="The character name")
    party_id: int = Field(title="The character's party id")


class RestrictedCharacterSchema(CharacterSchema):
    """The details of a character, excluding the player"""

    player: PlayerSchema = Field(exclude=True)
    data: CharacterSheet = Field(exclude=True)
    equipment: list[EquippedItemSchema] = Field(exclude=True)
    spellbook: list[RestrictedKnownSpellSchema] = Field(exclude=True)


class CharacterSchemaNoEmbeddedFields(BaseSchema):
    """The details of a character, excluding the party"""

    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(max_length=255, title="The character slug, used to identify it in the API")
    level: int | None = Field(ge=1, le=20, title="The character level", default=None)
    player: PlayerSchema = Field(title="The embedded character's player schema")


class ListCharacterSchema(BaseORMSchema):
    id: int = Field(ge=1, title="The character primary key in database")
    name: str = Field(max_length=255, title="The character name")
    slug: str = Field(max_length=255, title="The character slug, used to identify it in the API")
    player: PlayerSchema = Field(title="The embedded character's player schema")
    party: PartySchema = Field(title="The embedded character's party schema")


class UpdateCharacterSchema(BaseUpdateSchema):
    name: str | None = Field(title="A new character name (Optional)", default=None)
    data: dict | None = Field(title="Updates to the character sheet fields (Optional)", default=None)


class SearchResult(BaseSchema):
    rank: float
    resource_id: int
    language: str
    name: str


DisplayPlayerSchema.model_rebuild()
DisplayPartySchema.model_rebuild()
