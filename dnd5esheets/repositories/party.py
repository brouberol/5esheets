from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Character, Party, Player
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdatePartySchema


class PartyRepository(BaseRepository):
    model = Party

    @classmethod
    async def list_all(
        cls, session: AsyncSession, owner_id: int | None
    ) -> Sequence[Party]:
        result = await session.execute(
            select(Party)
            .join(Character, Party.members)
            .join(Player, Character.player)
            .filter(Player.id == owner_id)
        )
        return result.scalars().all()

    @classmethod
    async def get_by_id_if_member_of(
        cls, session: AsyncSession, id: int, member_id: int | None
    ) -> Party:
        """Return a Party given an argument id if it is owned by the argument player id"""
        query = (
            select(Party)
            .join(Character, Party.members)
            .join(Player, Character.player)
            .filter(Party.id == id)
        )
        if member_id is not None:
            query = query.filter(Player.id == member_id)
        result = await session.execute(query)
        return cls.one_or_raise_model_not_found(result)

    @classmethod
    async def update_if_member_of(
        cls,
        session: AsyncSession,
        id: int,
        body: UpdatePartySchema,
        member_id: int | None,
    ) -> Party:
        party = await cls.get_by_id_if_member_of(
            session=session, id=id, member_id=member_id
        )

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        party.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(party)
        await session.commit()

        return party
