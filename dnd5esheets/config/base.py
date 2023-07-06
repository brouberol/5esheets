from pathlib import Path

from pydantic import BaseSettings

db_dir = Path(__file__).parent.parent / "db"
db_file = db_dir / "5esheets.db"


class CommonSettings(BaseSettings):
    # used by fastapi-jwt-auth
    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 60 * 60 * 12  # 12h, in seconds
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect = True

    MULTITENANT_ENABLED: bool = False
    DB_URI: str = f"sqlite:///{db_file}"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_file}"
    SQLALCHEMY_ECHO: bool = False
    FRONTEND_CORS_ORIGIN = "http://localhost:3000"
