"""
Repositories are the layer through which we communicate with the database.

Any database access outside of repositories (eg: in the app routes) is strongly
discouraged.

"""
from typing import Self, Type, cast

from sqlalchemy.engine import Result

from dnd5esheets.models import BaseModel


class ModelNotFound(Exception):
    @classmethod
    def from_model_name(cls, model_name: str) -> Self:
        return cls(f"{model_name} not found")


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
