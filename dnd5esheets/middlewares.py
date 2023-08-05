from pathlib import Path

from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from pyinstrument import Profiler

from . import ExtendedFastAPI

current_dir = Path(__file__).parent


def register_middlewares(app: ExtendedFastAPI):
    if app.settings.FRONTEND_CORS_ORIGIN is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[app.settings.FRONTEND_CORS_ORIGIN],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    if app.settings.PROFILING_ENABLED is True:

        @app.middleware("http")
        async def profile_request(request: Request, call_next):
            """Profile the current request

            Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
            with slight improvements.

            """
            if request.query_params.get("profile", False):
                with Profiler(interval=0.0001, async_mode="enabled") as profiler:
                    await call_next(request)
                with open(current_dir / "../profile.html", "w") as out:
                    out.write(profiler.output_html())
            return await call_next(request)
