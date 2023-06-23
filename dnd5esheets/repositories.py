"""
Repositories are the layer through which we communicate with the database.

Any database access outside of repositories (eg: in the app routes) is strongly
discouraged.

"""

from sqlalchemy import select
from sqlalchemy.orm import defer, joinedload
from sqlalchemy.engine import Result
from .models import Character, BaseModel
from .schemas import UpdateCharacterSchema
from sqlalchemy.ext.asyncio import AsyncSession


class ModelNotFound(Exception):
    ...


class BaseRepository:
    model: BaseModel = None

    @classmethod
    def one_or_raise(cls, result: Result) -> BaseModel | None:
        """Return the one result from the argument query or raise a ModelNotFound exception if empty"""
        if model := result.scalars().one_or_none():
            return model
        raise ModelNotFound(f"{cls.model.__name__} not found")


class CharacterRepository(BaseRepository):
    model = Character

    @classmethod
    async def list_all(cls, session: AsyncSession) -> list[Character]:
        """List all existing characters, with their associated related data"""
        result = await session.execute(
            select(Character)
            # exclude the large json payload
            .options(joinedload(Character.player), joinedload(Character.party))
            # efficiently join the player and party tables
            .options(defer(Character.data))
        )
        return result.scalars().all()

    @classmethod
    async def get_by_slug(cls, session: AsyncSession, slug: str) -> Character | None:
        """Return a Character given an argument slug"""
        result = await session.execute(
            select(Character)
            .options(joinedload(Character.player), joinedload(Character.party))
            .filter(Character.slug == slug)
        )
        return cls.one_or_raise(result)

    @classmethod
    async def update_character(
        cls, session: AsyncSession, slug: str, body: UpdateCharacterSchema
    ) -> Character:
        character = await CharacterRepository.get_by_slug(session, slug)

        # Any non-nil field should be taken as the new value
        fields_to_update = {
            field: val for field, val in body.dict().items() if val is not None
        }

        character.update_from_dict(fields_to_update)

        # Persist the changes
        session.add(character)
        await session.commit()

        return character
