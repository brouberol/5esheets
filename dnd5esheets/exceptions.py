from typing import Self

from fastapi import HTTPException


class CacheHit(HTTPException):
    """Exception raised when a requested resource's ETag matches the If-None-Match request header"""


class RepositoryException(Exception):
    ...


class ModelNotFound(RepositoryException):
    @classmethod
    def from_model_name(cls, model_name: str) -> Self:
        return cls(f"{model_name} not found")


class DuplicateModel(RepositoryException):
    ...
