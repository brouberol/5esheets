from .base import CommonSettings
from pydantic_settings import SettingsConfigDict


class ProdSettings(CommonSettings):
    AUTHJWT_SECRET_KEY: str
    DB_URI: str
    DB_ASYNC_URI: str
    MULTITENANT_ENABLED: bool = True
    FRONTEND_CORS_ORIGIN: str | None = None
    model_config = SettingsConfigDict(env_file=".env")
