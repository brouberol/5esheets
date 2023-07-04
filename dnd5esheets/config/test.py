from .base import CommonSettings, db_dir


class TestSettings(CommonSettings):
    authjwt_secret_key: str = (
        "6ba4e05e642a4124ffb4a60435e37832296b74aefd078c45b4466d90684522d8"
    )
    DB_URI: str = f"sqlite:///{db_dir}/5esheets.test.db"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_dir}/5esheets.test.db"
    MULTITENANT_ENABLED: bool = True
