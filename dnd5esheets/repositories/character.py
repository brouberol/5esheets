from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from dnd5esheets.models import Character, Player
from dnd5esheets.repositories import BaseRepository
from dnd5esheets.schemas import UpdateCharacterSchema


class CharacterRepository(BaseRepository):
    model = Character

    @classmethod
    async def list_all(
        cls, session: AsyncSession, owner_id: int | None
    ) -> Sequence[Character]:
        """List all existing characters, with their associated related data"""
        query = select(Character).options(
            defer(Character.data)
        )  # exclude the large json payload
        if owner_id is not None:
            query = query.filter(Character.player_id == owner_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_slug(cls, session: AsyncSession, slug: str) -> Character:
        """Return a Character given an argument slug"""
        result = await session.execute(select(Character).filter(Character.slug == slug))
        return cls.one_or_raise_model_not_found(result)  # type: ignore

    @classmethod
    async def get_by_slug_if_owned(
        cls, session: AsyncSession, slug: str, owner_id: int | None
    ) -> Character:
        """Return a Character given an argument slug"""
        character = await cls.get_by_slug(session, slug)
        if owner_id is not None and character.player_id != owner_id:
            cls.raise_model_not_found()
        return character

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        slug: str,
        body: UpdateCharacterSchema,
    ) -> Character:
        character = await cls.get_by_slug(session, slug)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        character.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(character)
        await session.commit()

        return character
