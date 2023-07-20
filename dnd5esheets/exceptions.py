from fastapi import HTTPException


class CacheHit(HTTPException):
    """Exception raised when a requested resource's ETag matches the value of the If-None-Match request header"""
