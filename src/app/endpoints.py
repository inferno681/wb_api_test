from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.schemes import BaseRequest

router = APIRouter()


@router.post('/products')
async def get_product(
    data: BaseRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    await request.app.state.service.collect_data(data.artikul, session)
    return {'response': 'good'}
