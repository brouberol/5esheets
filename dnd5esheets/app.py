from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from .repositories import ModelNotFound
from .api import api


app = FastAPI()
app.include_router(api)


@app.exception_handler(ModelNotFound)
def raise_404_exception_on_model_not_found(_: Request, exc: Exception):
    """Return a 404 response when handling a ModelNotFound exception"""
    return JSONResponse(content={"detail": str(exc)}, status_code=404)
