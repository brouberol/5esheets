import json
from collections import defaultdict

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    ...


class NameReprMixin:
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"


class Player(NameReprMixin, BaseModel):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    characters: Mapped["Character"] = relationship(
        back_populates="player", cascade="all, delete-orphan"
    )


class Party(NameReprMixin, BaseModel):
    __tablename__ = "party"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    members: Mapped["Character"] = relationship(
        back_populates="party", cascade="all, delete-orphan"
    )


class Character(NameReprMixin, BaseModel):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    class_: Mapped[str] = mapped_column(String(80), name="class")
    level: Mapped[int] = mapped_column(Integer)
    json_data: Mapped[str] = mapped_column(Text)
    player_id: Mapped[int] = mapped_column(ForeignKey("player.id"))
    player: Mapped[Player] = relationship(back_populates="characters")
    party_id: Mapped[int] = mapped_column(ForeignKey("party.id"))
    party: Mapped[Party] = relationship(back_populates="members")

    # TODO: investigate hybrid_property to make sure json encoding/decoding is always done DB side? Or implement a Json type for sqlite?
    @property
    def data(self):
        d = defaultdict(str)
        d.update(json.loads(self.json_data))
        return d
