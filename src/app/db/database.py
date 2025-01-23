from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


engine = create_async_engine(
    url='postgresql+asyncpg://postgres:password@localhost:5432/postgres',
    echo=True,
)

async_session = async_sessionmaker(bind=engine)


async def get_async_session():
    """Async session generator."""
    async with async_session() as session:
        yield session
