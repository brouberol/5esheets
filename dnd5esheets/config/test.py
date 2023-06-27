from .base import CommonSettings, db_dir


class TestSettings(CommonSettings):
    DB_URI: str = f"sqlite:///{db_dir}/5esheets.test.db"
    DB_ASYNC_URI: str = f"sqlite+aiosqlite:///{db_dir}/5esheets.test.db"
