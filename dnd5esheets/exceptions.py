from typing import Self

from fastapi import HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import ORJSONResponse as JSONResponse
from starlette import status

from . import ExtendedFastAPI
from .config import Env


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


def register_exception_handlers(app: ExtendedFastAPI):
    @app.exception_handler(ModelNotFound)
    def raise_404_exception_on_model_not_found(_: Request, exc: Exception):
        """Return a 404 response when handling a ModelNotFound exception"""
        return JSONResponse(
            content={"detail": str(exc)}, status_code=status.HTTP_404_NOT_FOUND
        )

    @app.exception_handler(DuplicateModel)
    def raise_400_exception_on_duplicate_model(_: Request, exc: Exception):
        """Return a 400 response when handling a DuplicateModel exception"""
        return JSONResponse(
            content={"detail": str(exc)}, status_code=status.HTTP_400_BAD_REQUEST
        )

    @app.exception_handler(CacheHit)
    def cachehit_exception_handler(_: Request, exc: CacheHit):
        """Generate a correct 304 response when handling a CacheHit exception"""
        return Response("", status_code=exc.status_code, headers=exc.headers)

    if app.env != Env.prod:

        @app.exception_handler(ResponseValidationError)
        async def validation_exception_handler(
            _: Request, exc: ResponseValidationError
        ):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder({"detail": exc.errors()}),
            )
