from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import KnownSpell
from dnd5esheets.repositories import BaseRepository


class KnownSpellRepository(BaseRepository):
    model = KnownSpell

    @classmethod
    async def get_by_id_if_owned(
        cls, session: AsyncSession, id: int, owner_id: int
    ) -> KnownSpell:
        query = select(KnownSpell).filter(
            KnownSpell.id == id, KnownSpell.character_id == owner_id
        )
        result = await session.execute(query)
        return cast(KnownSpell, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def change_prepared_status(
        cls, session: AsyncSession, id: int, owner_id: int, prepared: bool
    ):
        known_spell = await cls.get_by_id_if_owned(session, id=id, owner_id=owner_id)
        known_spell.prepared = prepared
        session.add(known_spell)
        await session.commit()
        await session.refresh(known_spell)
        return known_spell
