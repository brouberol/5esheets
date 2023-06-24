from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    JWT_ENCODING_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # in mins
