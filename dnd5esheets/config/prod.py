from pydantic_settings import SettingsConfigDict

from .base import CommonSettings, LogFormat


class ProdSettings(CommonSettings):
    AUTHJWT_SECRET_KEY: str
    DB_URI: str
    DB_ASYNC_URI: str
    MULTITENANT_ENABLED: bool = True
    FRONTEND_CORS_ORIGIN: str | None = None
    DOCS_URL: str | None = None
    REDOC_URL: str | None = None
    OPENAPI_URL: str | None = None
    model_config = SettingsConfigDict(env_file=".env")
    LOG_FORMAT: LogFormat = "json"
