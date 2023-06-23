"""
Repositories are the layer through which we communicate with the database.

Any database access outside of repositories (eg: in the app routes) is strongly
discouraged.

"""
from typing import Type

from sqlalchemy.engine import Result

from dnd5esheets.models import BaseModel


class ModelNotFound(Exception):
    ...


class BaseRepository:
    model: Type[BaseModel] = BaseModel

    @classmethod
    def one_or_raise(cls, result: Result) -> BaseModel:
        """Return the result from the argument query or raise a ModelNotFound exception if empty"""
        if model := result.scalars().one_or_none():
            return model
        raise ModelNotFound(f"{cls.model.__name__} not found")
