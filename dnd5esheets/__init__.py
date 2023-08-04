from fastapi import FastAPI

from .config import Env
from .config.base import CommonSettings


class ExtendedFastAPI(FastAPI):
    def __init__(self, settings: CommonSettings, env: Env, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings
        self.env = env
