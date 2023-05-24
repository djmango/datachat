from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TrailingSlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.endswith('/') and request.url.path != '/':
            # Remove the trailing slash directly in the request's scope
            request.scope["path"] = request.scope["path"].rstrip('/')
        response = await call_next(request)
        return response
