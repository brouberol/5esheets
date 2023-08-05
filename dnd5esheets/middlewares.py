from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware
from fastapi_profiler import PyInstrumentProfilerMiddleware

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
            PyInstrumentProfilerMiddleware,
            server_app=app,
            is_print_each_request=False,
            async_mode="enable",
            html_file_name=current_dir / "../profile.html",
            open_in_browser=True,
            profiler_output_type="html",
        )
