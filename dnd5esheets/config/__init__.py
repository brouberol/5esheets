import os
from enum import StrEnum
from functools import lru_cache

from .dev import DevSettings
from .prod import ProdSettings
from .test import TestSettings


class Env(StrEnum):
    prod = "prod"
    dev = "dev"
    test = "test"


def get_env():
    return os.getenv("DND5ESHEETS_ENV")


@lru_cache
def get_settings():
    match get_env():
        case Env.prod:
            return ProdSettings()
        case Env.test:
            return TestSettings()
        case _:
            return DevSettings()
