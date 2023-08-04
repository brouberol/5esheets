from pathlib import Path
from typing import cast

from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles

from . import ExtendedFastAPI

dist_dir = Path(__file__).parent / "front" / "dist"


class SPAStaticFiles(StaticFiles):
    """Return a static file OR the root index.html file"""

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        # Theoretically, we shoud catch a HTTPException, but when we do
        # we get intercepted by starlette's AsyncExitStackMiddleware, and
        # immediately return a 404 response.
        except Exception as exc:
            exc = cast(HTTPException, exc)
            if exc.status_code != 404:
                raise exc
            else:
                # We serve the SPA root page
                return await super().get_response(".", scope)


def register_spa(app: ExtendedFastAPI):
    if dist_dir.exists():
        app.mount("", SPAStaticFiles(directory=dist_dir, html=True), name="static")
