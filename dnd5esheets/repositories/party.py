from typing import Sequence, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Character, Party, Player
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdatePartySchema


class PartyRepository(BaseRepository):
    model = Party

    @classmethod
    async def list_all(cls, session: AsyncSession, owner_id: int | None = None) -> Sequence[Party]:
        query = select(Party)
        if owner_id:
            query = (
                query.join(Character, Party.members)
                .join(Player, Character.player)
                .filter(Player.id == owner_id)
            )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        id: int,
        body: UpdatePartySchema,
    ) -> Party:
        party = await cls.get_by_id(session=session, id=id)

        # Any non-nil field should be taken as the new value
        fields_to_update = {field: val for field, val in body.model_dump().items() if val is not None}

        party.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(party)
        await session.commit()
        await session.refresh(party)

        return cast(Party, party)
