import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.endpoints import router as router_v1
from app.service import APIService, scheduler
from config import config

log = logging.getLogger('uvicorn')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Service initialization."""

    service = APIService()
    scheduler.start()
    app.state.service = service
    log.info('Service initialized')

    yield

    scheduler.shutdown()
    log.info('service stopped')


app = FastAPI(
    title=config.service.title,
    description=config.service.description,
    debug=config.service.debug,
    lifespan=lifespan,
)

app.include_router(router_v1, prefix='/api')


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=config.service.host,
        port=config.service.port,
    )
