from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import config

engine = create_async_engine(
    url=config.async_db_url,
    echo=config.db.echo,
)

sync_engine = create_engine(
    url=config.sync_db_url,
    echo=config.db.echo,
)

async_session = async_sessionmaker(bind=engine)


async def get_async_session():
    """Async session generator."""
    async with async_session() as session:
        yield session
