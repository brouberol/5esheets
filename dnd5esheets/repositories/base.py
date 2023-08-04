"""
Repositories are the layer through which we communicate with the database.

Any database access outside of repositories (eg: in the app routes) is strongly
discouraged.

"""
from typing import Type, cast

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.exceptions import ModelNotFound
from dnd5esheets.models import BaseModel


class BaseRepository:
    model: Type[BaseModel] = BaseModel

    @classmethod
    def raise_exc(cls, exc):
        raise exc.from_model_name(cls.model.__name__)

    @classmethod
    def raise_model_not_found(cls):
        cls.raise_exc(ModelNotFound)

    @classmethod
    def one_or_raise_model_not_found(cls, result: Result) -> BaseModel:
        """Return the result from the argument query or raise a ModelNotFound exception if empty"""
        if not (model := result.scalars().unique().one_or_none()):
            cls.raise_model_not_found()
        return cast(BaseModel, model)

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> BaseModel:
        """Return the repository model instance identified by the argument id"""
        query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        return cast(BaseModel, cls.one_or_raise_model_not_found(result))

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int):
        """Delete the repository model instance identified by the argument id"""
        model = await cls.get_by_id(session, id=id)
        await session.delete(model)
        await session.commit()
