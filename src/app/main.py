import logging

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI


from app.service import APIService
from app.endpoints import router

log = logging.getLogger('uvicorn')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Service initialization."""

    service = APIService()
    app.state.service = service
    log.info('Service initialized')

    yield

    await service.aclose()
    log.info('service stopped')


app = FastAPI(
    title='Service',
    description='Service description',
    debug=True,
    lifespan=lifespan,
)

app.include_router(router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='localhost',
        port=8000,
    )
