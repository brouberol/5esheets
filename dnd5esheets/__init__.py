from fastapi import FastAPI

from .config import Env
from .config.base import CommonSettings


class ExtendedFastAPI(FastAPI):
    settings: CommonSettings
    env: Env
