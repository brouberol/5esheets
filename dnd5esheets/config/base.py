from datetime import timedelta
from pathlib import Path
from typing import Literal, TypeAlias

from pydantic_settings import BaseSettings

db_dir = Path(__file__).parent.parent / "db"
db_file = db_dir / "5esheets.db"

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LogFormat: TypeAlias = Literal["plain", "json", "uvicorn"]


class CommonSettings(BaseSettings):
    # used by fastapi-jwt-auth
    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=12)

    MULTITENANCY_ENABLED: bool = False
    DB_URI: str = f"sqlite:///{db_file}"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_file}"
    SQLALCHEMY_ECHO: bool = False
    FRONTEND_CORS_ORIGIN: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    PROFILING_ENABLED: bool = False
    OPENAPI_URL: str | None = "/openapi.json"
    DOCS_URL: str | None = "/docs"
    REDOC_URL: str | None = "/redoc"
    LOG_LEVEL: LogLevel = "INFO"
    LOG_FORMAT: LogFormat = "plain"
    LOG_DEBUG: bool = False
