from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Item
from dnd5esheets.repositories import BaseRepository


class ItemRepository(BaseRepository):
    model = Item

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> Item:
        query = select(Item).filter(Item.id == id)
        result = await session.execute(query)
        return cast(Item, cls.one_or_raise_model_not_found(result))
