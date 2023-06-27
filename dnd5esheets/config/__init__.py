import os
from functools import lru_cache

from .dev import DevSettings
from .prod import ProdSettings
from .test import TestSettings


@lru_cache
def get_settings():
    match os.getenv("DND5ESHEETS_ENV"):
        case "prod":
            return ProdSettings()
        case "test":
            return TestSettings()
        case _:
            return DevSettings()
