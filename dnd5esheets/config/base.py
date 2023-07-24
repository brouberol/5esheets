from pathlib import Path
from datetime import timedelta

from pydantic import BaseSettings

db_dir = Path(__file__).parent.parent / "db"
db_file = db_dir / "5esheets.db"


class CommonSettings(BaseSettings):
    # used by fastapi-jwt-auth
    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=12)

    MULTITENANT_ENABLED: bool = False
    DB_URI: str = f"sqlite:///{db_file}"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_file}"
    SQLALCHEMY_ECHO: bool = False
    FRONTEND_CORS_ORIGIN: str | None = "http://localhost:3000"
