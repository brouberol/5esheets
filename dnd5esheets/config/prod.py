from .base import CommonSettings


class ProdSettings(CommonSettings):
    authjwt_secret_key: str
    authjwt_cookie_samesite: str = "lax"
    DB_URI: str
    DB_ASYNC_URI: str
    MULTITENANT_ENABLED: bool = True

    class Config:
        env_file = ".env"
