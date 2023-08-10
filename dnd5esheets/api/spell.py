from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session
from dnd5esheets.etag import handle_model_etag
from dnd5esheets.repositories.spell import SpellRepository
from dnd5esheets.schemas import SearchResult, SpellSchema

spell_api = APIRouter(prefix="/spell", tags=["spell"])


@spell_api.get("/search", response_model=list[SearchResult])
async def search_spells(
    search_term: str,
    favored_language: str | None = None,
    limit: int = 10,
    session: AsyncSession = Depends(create_scoped_session),
):
    return await SpellRepository.search(
        session, search_term=search_term, favored_language=favored_language, limit=limit
    )


@spell_api.get("/{id}", response_model=SpellSchema)
async def get_spell(
    id,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(create_scoped_session),
):
    """Return all details of a given spell."""
    spell = await SpellRepository.get_by_id(session, id=id)
    await handle_model_etag(
        request,
        response,
        model=spell,
    )
    return spell
