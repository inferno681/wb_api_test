from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from app.db.models import Product
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.schemes import BaseResponseCheck


header_scheme = APIKeyHeader(name='Authorization')


class APIService:
    """Base service."""

    def __init__(self):
        """Client initialization."""
        self.client = AsyncClient()
        self.BASE_URL = (
            'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub'
            '&dest=-1257786&spp=30&nm='
        )

    async def get_data(self, article: int) -> dict:
        """Get data request method."""
        url = f'{self.BASE_URL}{article}'
        response = await self.client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Error',
            )
        data = response.json()['data']['products'][0]
        if data == []:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='No data',
            )
        return data

    def check_data(self, data: dict) -> BaseResponseCheck:
        """Check data request method."""
        data['artikul'] = data['id']
        return BaseResponseCheck(**data)

    async def write_to_db(
        self,
        data: BaseResponseCheck,
        session: AsyncSession,
    ) -> dict:
        """Write to db method."""
        data = data.model_dump()
        await session.execute(
            insert(Product)
            .values(**data)
            .on_conflict_do_update(index_elements=['artikul'], set_=data)
        )
        await session.commit()
        return data

    async def collect_data(self, article: int, session: AsyncSession) -> dict:
        """Collect data method."""
        data = await self.get_data(article)
        data = self.check_data(data)
        data = await self.write_to_db(data, session)
        return data

    async def aclose(self):
        """Client closing method."""
        await self.client.aclose()
