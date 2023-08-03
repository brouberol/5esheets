from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.etag import handle_model_etag
from dnd5esheets.repositories.spell import SpellRepository
from dnd5esheets.schemas import SpellSchema

spell_api = APIRouter(prefix="/spell", tags=["spell"])


@spell_api.get("/{id}", response_model=SpellSchema)
async def get_spell(
    id,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(create_scoped_session),
):
    await handle_model_etag(
        request,
        response,
        model=await SpellRepository.get_by_id(session, id=id),
        repository=SpellRepository,
    )
    return await SpellRepository.get_by_id(session, id=id)
