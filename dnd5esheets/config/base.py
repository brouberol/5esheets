from pathlib import Path

from pydantic import BaseSettings

db_dir = Path(__file__).parent.parent / "db"
db_file = db_dir / "5esheets.db"


class CommonSettings(BaseSettings):
    JWT_ENCODING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 12 * 60  # in mins
    MULTITENANT_ENABLED: bool = False
    DB_URI: str = f"sqlite:///{db_file}"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_file}"
    SQLALCHEMY_ECHO: bool = False
