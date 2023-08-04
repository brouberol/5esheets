from fastapi.middleware.cors import CORSMiddleware

from . import ExtendedFastAPI


def register_middlewares(app: ExtendedFastAPI):
    if app.settings.FRONTEND_CORS_ORIGIN is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[app.settings.FRONTEND_CORS_ORIGIN],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
