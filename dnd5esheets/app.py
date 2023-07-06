from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_jwt_auth.exceptions import AuthJWTException

from .api import api
from .config import get_settings
from .repositories import ModelNotFound

app = FastAPI()
settings = get_settings()
app.include_router(api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_CORS_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
dist_dir = Path(__file__).parent / "front" / "dist"


@app.exception_handler(ModelNotFound)
def raise_404_exception_on_model_not_found(_: Request, exc: Exception):
    """Return a 404 response when handling a ModelNotFound exception"""
    return JSONResponse(content={"detail": str(exc)}, status_code=404)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(_: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if dist_dir.exists():
    app.mount("", StaticFiles(directory=dist_dir, html=True), name="static")
