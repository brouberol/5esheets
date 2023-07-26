from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from .admin import register_admin
from .api import api
from .config import get_settings
from .db import async_engine
from .exceptions import CacheHit
from .repositories import DuplicateModel, ModelNotFound

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
    return JSONResponse(content={"detail": str(exc)}, status_code=404)


@app.exception_handler(DuplicateModel)
def raise_400_exception_on_duplicate_model(_: Request, exc: Exception):
    """Return a 400 response when handling a DuplicateModel exception"""
    return JSONResponse(content={"detail": str(exc)}, status_code=400)


# Generate a correct 304 response when handling a CacheHit exception.
@app.exception_handler(CacheHit)
def cachehit_exception_handler(_: Request, exc: CacheHit):
    return Response("", status_code=exc.status_code, headers=exc.headers)


if dist_dir.exists():
    app.mount("", StaticFiles(directory=dist_dir, html=True), name="static")
