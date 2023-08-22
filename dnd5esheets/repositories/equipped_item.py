from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import EquippedItem
from dnd5esheets.repositories import BaseRepository


class EquippedItemRepository(BaseRepository):
    model = EquippedItem

    @classmethod
    async def get_by_id_if_owned(
        cls, session: AsyncSession, id: int, owner_id: int
    ) -> EquippedItem:
        query = select(EquippedItem).filter(
            EquippedItem.id == id, EquippedItem.character_id == owner_id
        )
        result = await session.execute(query)
        return cast(EquippedItem, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def change_equipped_status(
        cls, session: AsyncSession, id: int, equipped: bool
    ):
        equipped_item = await cls.get_by_id(session, id=id)
        equipped_item.equipped = equipped
        session.add(equipped_item)
        await session.commit()
        await session.refresh(equipped_item)
        return equipped_item
