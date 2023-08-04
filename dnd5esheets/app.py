from fastapi import FastAPI

from .admin import register_admin
from .api import register_api
from .config import get_env, get_settings
from .db import async_engine
from .exceptions import register_exception_handlers
from .middleware import register_middlewares
from .spa import register_spa


def create_app() -> FastAPI:
    app = FastAPI()
    app.settings = get_settings()
    app.env = get_env()

    register_api(app)
    register_middlewares(app)
    register_exception_handlers(app)
    register_admin(app, async_engine)
    register_spa(app)
    return app
