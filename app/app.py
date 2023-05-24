import os
from pathlib import Path

import uvicorn

# from app.handlers.exception_handler import exception_handler
from app.middlewares.correlation_id_middleware import CorrelationIdMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.middlewares.trailing_slash_middleware import TrailingSlashMiddleware
from app.routes import helloworld_router
                        
from fastapi import FastAPI

# Setup
HERE = Path(__file__).parent
DEBUG = True if os.getenv('DEBUG') == '1' else False

app = FastAPI(title='DataChat API', description='BUILDSPACE', version="0.1.0", debug=DEBUG)

# app.add_exception_handler(Exception, exception_handler)

# Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
app.add_middleware(LoggingMiddleware)
# app.add_middleware(TrailingSlashMiddleware)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(helloworld_router.router, prefix='/hello', tags=['Hello'])

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)