from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Spell
from dnd5esheets.repositories import BaseRepository


class SpellRepository(BaseRepository):
    model = Spell

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Spell:
        query = select(Spell).filter(Spell.id == id)
        result = await session.execute(query)
        return cast(Spell, cls.one_or_raise_model_not_found(result))
