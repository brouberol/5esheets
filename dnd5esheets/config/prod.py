from .base import CommonSettings


class ProdSettings(CommonSettings):
    SECRET_KEY: str

    class Config:
        env_file = ".env"
