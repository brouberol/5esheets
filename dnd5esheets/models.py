import json
from copy import deepcopy
from datetime import datetime
from typing import Self

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


# Taken from https://stackoverflow.com/a/49933601
class Json(TypeDecorator):
    @property
    def python_type(self):
        return object

    impl = types.Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_literal_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return None


def pascal_to_snake(pascal_string):
    snake = []
    for i, char in enumerate(pascal_string):
        if char.isupper() and i != 0:
            snake += "_"
        snake += char.lower()
    return "".join(snake)


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init_subclass__(cls) -> None:
        cls.__tablename__ = pascal_to_snake(cls.__name__)
        return super().__init_subclass__()

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


class NameReprMixin:
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


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


class EquippedItem(BaseModel):
    amount: Mapped[int] = mapped_column(Integer, default=1)
    equipped: Mapped[bool] = mapped_column(Boolean, default=False)

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped[Item] = relationship(lazy="joined")

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    owner: Mapped["Character"] = relationship(back_populates="equipment", lazy="joined")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.item}>"


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
    )
    party_id: Mapped[int] = mapped_column(ForeignKey("party.id"))
    party: Mapped[Party] = relationship(
        back_populates="members",
        # always load the party via a joinedload
        lazy="joined",
    )
    equipment: Mapped[list[EquippedItem]] = relationship(
        back_populates="owner", lazy="selectin", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("slug", "player_id", name="character_slug_unique_per_player"),
    )


class Spell(NameReprMixin, BaseModel):
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    school: Mapped[str] = mapped_column(String(1), nullable=False)
    data: Mapped[str] = mapped_column(Json, name="json_data")

    @validates("level")
    def validate_level(self, key, level):
        if level not in range(0, 10):
            raise ValueError("Level should be between 0 and 9")
        return level
