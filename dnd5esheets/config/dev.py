from .base import CommonSettings


class DevSettings(CommonSettings):
    authjwt_secret_key: str = (
        "6ba4e05e642a4124ffb4a60435e37832296b74aefd078c45b4466d90684522d8"
    )
