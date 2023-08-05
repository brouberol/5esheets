from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi_cprofile.profiler import CProfileMiddleware

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
        app.add_middleware(
            CProfileMiddleware,
            server_app=app,
            enable=True,
            print_each_request=True,
            strip_dirs=False,
            sort_by="cumulative",
            filename=current_dir / ".." / "5esheets.pstats",
        )
