import json
import logging
import time
from pathlib import Path
from typing import Any, Callable

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer
from pyinstrument.renderers.speedscope import SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware

from dnd5esheets.config import Env

from . import ExtendedFastAPI

current_dir = Path(__file__).parent


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware in charge of logging the HTTP request and response

    Taken and adapted from https://medium.com/@dhavalsavalia/
    fastapi-logging-middleware-logging-requests-and-responses-with-ease-and-style-201b9aa4001a

    """

    def __init__(self, app: ExtendedFastAPI) -> None:
        super().__init__(app)
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        logging_dict: dict[str, Any] = {}

        await request.body()
        response, response_dict = await self._log_response(call_next, request)
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict
        logging_dict["correlation_id"] = request.headers["X-Request-ID"]

        self.logger.info(json.dumps(logging_dict))
        return response

    async def _log_request(self, request: Request) -> dict[str, Any]:
        """Logs request part
         Arguments:
        - request: Request

        """

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host if request.client is not None else None,
        }

        try:
            body = await request.json()
        except Exception:
            body = None
        else:
            request_logging["body"] = body

        return request_logging

    async def _log_response(
        self, call_next: Callable, request: Request
    ) -> tuple[Response, dict[str, Any]]:
        """Logs response part

        Arguments:
        - call_next: Callable (To execute the actual path function and get response back)
        - request: Request
        - request_id: str (uuid)
        Returns:
        - response: Response
        - response_logging: str
        """

        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request)
        finish_time = time.perf_counter()
        execution_time = finish_time - start_time

        overall_status = "successful" if response.status_code < 400 else "failed"

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s",
        }
        return response, response_logging

    async def _execute_request(self, call_next: Callable, request: Request) -> Response:
        """Executes the actual path function using call_next.

        Arguments:
        - call_next: Callable (To execute the actual path function
                     and get response back)
        - request: Request
        - request_id: str (uuid)
        Returns:
        - response: Response
        """
        try:
            response: Response = await call_next(request)

        except Exception as e:
            self.logger.exception({"path": request.url.path, "method": request.method, "reason": e})
            raise e

        else:
            return response


def register_cors_middleware(app: ExtendedFastAPI):
    if app.settings.FRONTEND_CORS_ORIGIN is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=app.settings.FRONTEND_CORS_ORIGIN,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


def register_profiling_middleware(app: ExtendedFastAPI):
    if app.settings.PROFILING_ENABLED is True:

        @app.middleware("http")
        async def profile_request(request: Request, call_next):
            """Profile the current request

            Taken from https://pyinstrument.readthedocs.io/en/latest/guide.html#profile-a-web-request-in-fastapi
            with slight improvements.

            """
            profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
            profile_type_to_renderer = {
                "html": HTMLRenderer,
                "speedscope": SpeedscopeRenderer,
            }
            if request.query_params.get("profile", False):
                profile_type = request.query_params.get("profile_format", "speedscope")
                with Profiler(interval=0.001, async_mode="enabled") as profiler:
                    response = await call_next(request)
                extension = profile_type_to_ext[profile_type]
                renderer = profile_type_to_renderer[profile_type]()
                with open(current_dir / f"../profile.{extension}", "w") as out:
                    out.write(profiler.output(renderer=renderer))
                return response
            return await call_next(request)


def register_request_response_logging_middleware(app: ExtendedFastAPI):
    if app.env != Env.test:
        app.add_middleware(RequestResponseLoggingMiddleware)


def register_correlation_id_middleware(app: ExtendedFastAPI):
    app.add_middleware(CorrelationIdMiddleware)


def register_middlewares(app: ExtendedFastAPI):
    register_cors_middleware(app)
    register_correlation_id_middleware(app)
    register_request_response_logging_middleware(app)
    register_profiling_middleware(app)
