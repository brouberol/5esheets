from .base import CommonSettings


class DevSettings(CommonSettings):
    PROFILING_ENABLED: bool = True
    AUTHJWT_SECRET_KEY: str = (
        "6ba4e05e642a4124ffb4a60435e37832296b74aefd078c45b4466d90684522d8"
    )
