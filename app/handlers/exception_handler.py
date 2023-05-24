from app.logs import logger

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse



async def exception_handler(request: Request, exc: Exception):

    if isinstance(exc, HTTPException):
        logger.exception(exc, extra={'uuid': request.state.correlation_id, 'type': 'api-error'})
        return JSONResponse(
            status_code=exc.status_code,
            content={"uuid": request.state.correlation_id, "message": exc.detail, "exception": repr(exc)}
        )
    else:
        logger.exception(exc, extra={'uuid': request.state.correlation_id, 'type': 'app-error'})
        return JSONResponse(
            status_code=500,
            content={"uuid": request.state.correlation_id, "message": "An internal error has occurred", "exception": repr(exc)}
        )
