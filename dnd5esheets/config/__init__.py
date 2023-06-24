import os
from functools import lru_cache

from .dev import DevSettings
from .prod import ProdSettings


@lru_cache
def get_settings():
    if os.getenv("5ESHEETS_ENV") == "prod":
        return ProdSettings()
    return DevSettings()
