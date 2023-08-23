from typing import Sequence, cast

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Character, Party, Player
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdatePlayerSchema


class PlayerRepository(BaseRepository):
    model = Player

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Player:
        """Return a Player given an argument id"""
        result = await session.execute(select(Player).filter(Player.id == id))
        return cast(Player, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def get_by_email(cls, session: AsyncSession, email: str) -> Player:
        """Return a Player given an argument email"""
        result = await session.execute(select(Player).filter(Player.email == email))
        return cast(Player, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def update(
        cls, session: AsyncSession, id: int, body: UpdatePlayerSchema
    ) -> Player:
        player = await cls.get_by_id(session, id)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.model_dump().items() if val is not None
        }

        player.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(player)
        await session.commit()

        return player

    @classmethod
    async def player_has_character_in_party(
        cls, session: AsyncSession, player_id: int, party_id: int
    ) -> bool:
        """Return whether the argument player has at least one character in the given party"""
        return bool(
            await session.scalar(
                select(func.count())
                .select_from(Player)
                .join(Character)
                .join(Party)
                .filter(Player.id == player_id, Party.id == party_id)
            )
        )

    @classmethod
    async def get_all_players_with_characters_in_same_party_than_character(
        cls, session: AsyncSession, character_slug: str
    ) -> Sequence[Player]:
        """Return all players belonging to the same party than the argument character"""
        party_subquery = (
            select(Party.id)
            .join(Character)
            .join(Player)
            .filter(Character.slug == character_slug)
        )
        query = (
            select(Player)
            .join(Character)
            .join(Party)
            .filter(Party.id.in_(party_subquery))
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_all_players_with_characters_in_party(
        cls, session: AsyncSession, party_id: int, player_id: int | None = None
    ) -> Sequence[Player]:
        """Return all players belonging to the argument party"""
        query = select(Player).join(Character).join(Party).filter(Party.id == party_id)
        if player_id:
            query = query.filter(Player.id == player_id)
        result = await session.execute(query)
        return result.scalars().all()
