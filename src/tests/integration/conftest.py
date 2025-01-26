import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, drop_database

from config.config import config

config.db.name = 'test_db'


@pytest.fixture(scope='session')
def engine():
    return create_async_engine(url=config.async_db_url)


@pytest.fixture(scope='session', autouse=True)
async def crate_and_drop_database():
    """Database preparation  before test.."""
    from app.db import Base

    create_database(config.sync_db_url)

    engine = create_async_engine(url=config.async_db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
    drop_database(config.sync_db_url)
    await engine.dispose()


@pytest.fixture(scope='session')
def anyio_backend():
    """Backend for test."""
    return 'asyncio'


@pytest.fixture(scope='session')
async def client():
    """Client for testing."""
    from app.main import app

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url='http://127.0.0.1:8000/api/v1/',
        ) as client:
            yield client


@pytest.fixture
def request_data():
    return {'artikul': 211695539}


@pytest.fixture
def collect_data_url():
    return '/products'


@pytest.fixture
def subscription_url():
    return '/subscribe/211695539'


@pytest.fixture
def get_product_url():
    return '/products/211695539'
