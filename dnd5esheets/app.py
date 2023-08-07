from fastapi.responses import ORJSONResponse

from . import ExtendedFastAPI
from .admin import register_admin
from .api import register_api
from .config import get_env, get_settings
from .db import async_engine
from .exceptions import register_exception_handlers
from .logs import setup_logging
from .middlewares import register_middlewares
from .spa import register_spa


def create_app() -> ExtendedFastAPI:
    settings = get_settings()
    app = ExtendedFastAPI(
        default_response_class=ORJSONResponse,
        settings=settings,
        env=get_env(),
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
    )
    setup_logging(app)
    register_api(app)
    register_middlewares(app)
    register_exception_handlers(app)
    register_admin(app, async_engine)
    register_spa(app)
    return app
