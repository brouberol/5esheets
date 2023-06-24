from pathlib import Path

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .api import api
from .repositories import ModelNotFound

app = FastAPI()
app.include_router(api)

dist_dir = Path(__file__).parent / "front" / "dist"


@app.exception_handler(ModelNotFound)
def raise_404_exception_on_model_not_found(_: Request, exc: Exception):
    """Return a 404 response when handling a ModelNotFound exception"""
    return JSONResponse(content={"detail": str(exc)}, status_code=404)


app.mount("", StaticFiles(directory=dist_dir, html=True), name="static")
