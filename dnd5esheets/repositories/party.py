from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dnd5esheets.models import Party
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdatePartySchema


class PartyRepository(BaseRepository):
    model = Party

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Party:
        """Return a Party given an argument slug"""
        result = await session.execute(select(Party).filter(Party.id == id))
        return cls.one_or_raise(result)  # type: ignore

    @classmethod
    async def update(
        cls, session: AsyncSession, id: int, body: UpdatePartySchema
    ) -> Party:
        party = await cls.get_by_id(session, id)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        party.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(party)
        await session.commit()

        return party
