from pathlib import Path

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette import status

from .admin import register_admin
from .api import api
from .config import Env, get_env, get_settings
from .db import async_engine
from .exceptions import CacheHit, DuplicateModel, ModelNotFound
from .spa import SPAStaticFiles

app = FastAPI()
settings = get_settings()
app.include_router(api)


if settings.FRONTEND_CORS_ORIGIN is not None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_CORS_ORIGIN],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


register_admin(app, async_engine)

dist_dir = Path(__file__).parent / "front" / "dist"


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


if get_env() != Env.prod:

    @app.exception_handler(ResponseValidationError)
    async def validation_exception_handler(_: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )


if dist_dir.exists():
    app.mount("", SPAStaticFiles(directory=dist_dir, html=True), name="static")
