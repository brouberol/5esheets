import hashlib
from copy import deepcopy
from datetime import datetime
from enum import StrEnum
from typing import Self

import orjson
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    TypeDecorator,
    UniqueConstraint,
    types,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)


class Role(StrEnum):
    player = "player"
    gm = "gm"


# Taken from https://stackoverflow.com/a/49933601
class Json(TypeDecorator):
    @property
    def python_type(self):
        return object

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return orjson.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return orjson.loads(value)
        except (ValueError, TypeError):
            return None


class SqliteStrEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = String

    @property
    def python_type(self):
        return StrEnum

    def __init__(self, enumtype, *args, **kwargs):
        super(SqliteStrEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, str):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)


def pascal_to_snake(pascal_string):
    snake = []
    for i, char in enumerate(pascal_string):
        if char.isupper() and i != 0:
            snake += "_"
        snake += char.lower()
    return "".join(snake)


class BaseModel(DeclarativeBase):
    """A base model class, inherited from by all 5esheets models."""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init_subclass__(cls) -> None:
        # Infer the __tablename__ as the snake case conversion of the class name
        cls.__tablename__ = pascal_to_snake(cls.__name__)
        return super().__init_subclass__()

    def as_dict(self) -> dict:
        column_names_to_attr_name = {
            col.name: attr_name
            for attr_name, col in self.__mapper__._init_properties.items()
        }
        return {
            c.name: getattr(self, column_names_to_attr_name.get(c.name, c.name))
            for c in self.__table__.columns
        }

    def update_from_dict(self, fields_to_update: dict) -> Self:
        """Update all columns of a given model instance to the provided values.

        If a field maps to a Json column, the underlying JSON object will be updated.

        """

        def update_from_subdict(value: dict, target: dict) -> dict:
            for key, val in deepcopy(value).items():
                if isinstance(val, dict):
                    target[key] = update_from_subdict(val, target[key])
                else:
                    target[key] = val
            return target

        for field_name, value in fields_to_update.items():
            field_type = getattr(self.__class__, field_name).type.__class__
            if field_type is Json:
                new_value = deepcopy(getattr(self, field_name))  # a python dict
                new_value = update_from_subdict(value, new_value)
                setattr(self, field_name, new_value)
            else:
                setattr(self, field_name, value)
        return self

    def compute_etag(self):
        """Compute the model instance etag as the sha1 of its last update ISO datetime"""
        digest = hashlib.sha1()
        digest.update(self.updated_at.isoformat().encode("utf-8"))
        return digest.hexdigest()


class NameReprMixin:
    """Derive the instance repr and str from the class name"""

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"

    def __str__(self):
        return self.name


class Player(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    characters: Mapped[list["Character"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        # always load the characters through a selectinload, avoiding N+1 queries
        lazy="selectin",
    )
    player_roles: Mapped[list["PlayerRole"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class Party(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    members: Mapped[list["Character"]] = relationship(
        back_populates="party",
        cascade="all, delete-orphan",
        # always load the members through a selectinload, avoiding N+1 queries
        lazy="selectin",
    )


class Item(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    data: Mapped[str] = mapped_column(Json, name="json_data")

    @property
    def five_e_tools_url(self):
        return f"https://5e.tools/items.html#{self.name.lower()}_{self.data['source']['book'].lower()}"


class EquippedItem(BaseModel):
    amount: Mapped[int] = mapped_column(Integer, default=1)
    equipped: Mapped[bool] = mapped_column(Boolean, default=False)

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped[Item] = relationship(lazy="joined")

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    owner: Mapped["Character"] = relationship(back_populates="equipment", lazy="joined")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.item)}>"


class KnownSpell(BaseModel):
    prepared: Mapped[bool] = mapped_column(Boolean, default=False)
    spell_id: Mapped[int] = mapped_column(ForeignKey("spell.id"))
    spell: Mapped["Spell"] = relationship(lazy="joined")
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    caster: Mapped["Character"] = relationship(
        back_populates="spellbook", lazy="joined"
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {str(self.spell)}>"


class Character(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    class_: Mapped[str] = mapped_column(String(80), name="class", nullable=True)
    level: Mapped[int] = mapped_column(Integer, nullable=True)
    data: Mapped[str] = mapped_column(Json, name="json_data", nullable=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    player: Mapped[Player] = relationship(
        back_populates="characters",
        # always load the player via a joinedload
        lazy="joined",
        join_depth=2,
    )
    party_id: Mapped[int] = mapped_column(ForeignKey("party.id"))
    party: Mapped[Party] = relationship(
        back_populates="members",
        # always load the party via a joinedload
        lazy="joined",
        join_depth=2,
    )
    equipment: Mapped[list[EquippedItem]] = relationship(
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete-orphan",
        join_depth=2,
    )
    spellbook: Mapped[list[KnownSpell]] = relationship(
        back_populates="caster",
        lazy="selectin",
        cascade="all, delete-orphan",
        join_depth=2,
    )
    __table_args__ = (
        UniqueConstraint("slug", "player_id", name="character_slug_unique_per_player"),
    )

    @validates("level")
    def validate_character_level(self, key, level):
        if level is not None and level not in range(1, 21):
            raise ValueError("Level should be between 1 and 20")
        return level


class Spell(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    school: Mapped[str] = mapped_column(String(30), nullable=False)
    data: Mapped[str] = mapped_column(Json, name="json_data")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name} [{self.level}]>"

    @validates("level")
    def validate_level(self, key, level):
        if level not in range(0, 10):
            raise ValueError("Level should be between 0 and 9")
        return level

    @property
    def five_e_tools_url(self):
        return f"https://5e.tools/spells.html#{self.name.lower()}_{self.data['source']['book'].lower()}"


class PlayerRole(BaseModel):
    """The role a player has in a party (DM, player)"""

    role: Mapped[StrEnum] = mapped_column(SqliteStrEnum(Role), default=Role.player)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    player: Mapped[Player] = relationship(back_populates="player_roles", lazy="joined")
    party_id: Mapped[int] = mapped_column(ForeignKey("party.id"))
    party: Mapped[Party] = relationship(lazy="joined")

    __table_args__ = (
        UniqueConstraint("party_id", "player_id", name="party_id_unique_per_player_id"),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.party.name}/{self.player.name}: {self.role}>"

    def __str__(self):
        if self.party:
            return f"{self.role.capitalize()} in {self.party.name}"
        return self.role.capitalize()
