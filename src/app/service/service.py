from fastapi import HTTPException, status
from httpx import AsyncClient
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    ABSENT_SUBSCRIPTION_MESSAGE,
    DB_ERROR,
    EXIST_SUBSCRIPTION_MESSAGE,
    NO_DATA_ERROR,
    SUBSCRIPTION_ACTIVATION_MESSAGE,
    SUBSCRIPTION_DEACTIVATION_MESSAGE,
    UNEXPECTED_RESPONSE_ERROR,
)
from app.db import Product, get_async_session
from app.schemes import BaseResponseCheck
from app.service.scheduler import scheduler
from config import config


class APIService:
    """Base service."""

    def __init__(self):
        """Client initialization."""
        self.BASE_URL = config.service.base_url

    async def get_data(self, article: int) -> dict:
        """Get data request method."""
        url = f'{self.BASE_URL}{article}'
        async with AsyncClient() as client:
            response = await client.get(url)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=UNEXPECTED_RESPONSE_ERROR,
            )
        data = response.json().get('data', {}).get('products', [])
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=NO_DATA_ERROR.format(article=article),
            )
        return data[0]

    def check_data(self, data: dict) -> dict:
        """Check data request method."""
        data['artikul'] = data['id']
        return BaseResponseCheck(**data).model_dump()

    async def write_to_db(
        self,
        data: dict,
        session: AsyncSession,
    ) -> dict:
        """Write to db method."""
        result = await session.execute(
            insert(Product)
            .values(**data)
            .on_conflict_do_update(index_elements=['artikul'], set_=data)
            .returning(Product)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=DB_ERROR,
            )
        await session.commit()
        await session.refresh(product)
        return product.to_dict()

    async def run_task(self, article):
        async for session in get_async_session():
            await self.collect_data(article, session)

    async def collect_data(self, article: int, session: AsyncSession) -> dict:
        """Collect data method."""
        data = await self.get_data(article)
        data = self.check_data(data)
        data = await self.write_to_db(data, session)
        return data

    async def subscribe(self, article: int):
        """Subscribe method."""
        job_id = str(article)
        if scheduler.get_job(job_id):
            return {
                'message': EXIST_SUBSCRIPTION_MESSAGE.format(article=article)
            }

        scheduler.add_job(
            self.run_task,
            'interval',
            args=[article],
            minutes=30,
            id=job_id,
            replace_existing=True,
        )
        return {
            'message': SUBSCRIPTION_ACTIVATION_MESSAGE.format(article=article)
        }

    async def unsubscribe(self, article: int):
        """Unsubscribe method."""
        job_id = str(article)
        if not scheduler.get_job(job_id):
            return {
                'message': ABSENT_SUBSCRIPTION_MESSAGE.format(article=article)
            }
        scheduler.remove_job(job_id)
        return {
            'message': SUBSCRIPTION_DEACTIVATION_MESSAGE.format(
                article=article
            )
        }
