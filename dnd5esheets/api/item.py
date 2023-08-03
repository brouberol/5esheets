from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.item import ItemRepository
from dnd5esheets.schemas import ItemSchema

item_api = APIRouter(prefix="/item", tags=["item"])


@item_api.get("/{id}", response_model=ItemSchema)
async def get_item(id, session: AsyncSession = Depends(create_scoped_session)):
    return await ItemRepository.get_by_id(session, id=id)
