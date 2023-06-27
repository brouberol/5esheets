from .base import CommonSettings


class ProdSettings(CommonSettings):
    SECRET_KEY: str
    DB_URI: str
    DB_ASYNC_URI: str
    MULTITENANT_ENABLED: bool = True

    class Config:
        env_file = ".env"
