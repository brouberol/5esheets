import json
from typing import Self

from sqlalchemy import Boolean, ForeignKey, Integer, String, TypeDecorator, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


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


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    def update_from_dict(self, fields_to_update: dict) -> Self:
        """Update all columns of a given model instance to the provided values.

        If a field maps to a Json column, the underlying JSON object will be updated.

        """
        for field_name, value in fields_to_update.items():
            field_type = getattr(self.__class__, field_name).type.__class__
            if field_type is Json:
                new_value = getattr(self, field_name).copy()  # a python dict
                for key, val in value.items():
                    new_value[key] = val
                setattr(self, field_name, new_value)
            else:
                setattr(self, field_name, value)
        return self


class NameReprMixin:
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class Player(NameReprMixin, BaseModel):
    __tablename__ = "player"

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
    __tablename__ = "party"

    name: Mapped[str] = mapped_column(String(255))
    members: Mapped[list["Character"]] = relationship(
        back_populates="party",
        cascade="all, delete-orphan",
        # always load the members through a selectinload, avoiding N+1 queries
        lazy="selectin",
    )


class Item(NameReprMixin, BaseModel):
    __tablename__ = "item"

    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    data: Mapped[str] = mapped_column(Json, name="json_data")


class EquippedItem(BaseModel):
    __tablename__ = "equipped_item"

    amount: Mapped[int] = mapped_column(Integer, default=1)
    equipped: Mapped[bool] = mapped_column(Boolean, default=False)

    item_id: Mapped[int] = mapped_column(ForeignKey("item.id"))
    item: Mapped[Item] = relationship(lazy="joined")

    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))
    owner: Mapped["Character"] = relationship(back_populates="equipment", lazy="joined")


class Character(NameReprMixin, BaseModel):
    __tablename__ = "character"

    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    class_: Mapped[str] = mapped_column(String(80), name="class")
    level: Mapped[int] = mapped_column(Integer)
    data: Mapped[str] = mapped_column(Json, name="json_data")
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
