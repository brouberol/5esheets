from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.repositories.spell import SpellRepository
from dnd5esheets.schemas import SpellSchema

spell_api = APIRouter(prefix="/spell", tags=["spell"])


@spell_api.get("/{id}", response_model=SpellSchema)
async def get_spell(id, session: AsyncSession = Depends(create_scoped_session)):
    return await SpellRepository.get_by_id(session, id=id)
