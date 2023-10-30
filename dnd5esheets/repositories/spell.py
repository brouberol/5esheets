from pydantic.dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.models import Spell
from dnd5esheets.repositories import BaseRepository


@dataclass
class SpellSearchResult:
    rank: float
    resource_id: int
    language: str
    name: str
    description: str | None


class SpellRepository(BaseRepository):
    model = Spell

    search_fields = ["spell_id", "language", "name", "description"]

    @classmethod
    async def search(
        cls,
        session: AsyncSession,
        search_term: str,
        limit: int = 10,
        favored_language: str | None = None,
    ) -> list[SpellSearchResult]:
        results = [
            SpellSearchResult(*result)
            for result in await cls._search(session, search_term=search_term, limit=limit)
        ]
        if favored_language:
            results = sorted(
                results,
                # The lower the rank, the better the match, so we need to assign a lower weight
                # to the favored language
                key=lambda result: (
                    0 if result.language == favored_language else 1,
                    result.rank,
                ),
            )
        return results
