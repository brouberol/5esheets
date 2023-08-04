from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app: FastAPI):
    if app.settings.FRONTEND_CORS_ORIGIN is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[app.settings.FRONTEND_CORS_ORIGIN],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
