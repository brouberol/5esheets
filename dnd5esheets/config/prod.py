from .base import CommonSettings


class ProdSettings(CommonSettings):
    SECRET_KEY: str
    MULTITENANT_ENABLED: bool = True

    class Config:
        env_file = ".env"
