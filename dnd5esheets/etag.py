from fastapi import Request, Response

from .exceptions import CacheHit


def handle_etag_for_request(etag: str, request: Request, response: Response):
    """Raise a CacheHit exception if the provided etag matches the if-none-match request header.

    If no such header is provided, an 'ETag' header will be added to the response.

    """
    response.headers.update({"ETag": etag})
    if not request.headers.get("if-none-match"):
        return
    client_etag = request.headers["if-none-match"]
    if client_etag == etag:
        raise CacheHit(status_code=304, headers={"ETag": etag})
