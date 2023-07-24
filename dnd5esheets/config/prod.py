from .base import CommonSettings


class ProdSettings(CommonSettings):
    AUTHJWT_SECRET_KEY: str
    DB_URI: str
    DB_ASYNC_URI: str
    MULTITENANT_ENABLED: bool = True
    FRONTEND_CORS_ORIGIN: str | None = None

    class Config:
        env_file = ".env"
