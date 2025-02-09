from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemes import BaseRequest, BaseResponse, ResponseMessage

router = APIRouter(prefix='/v1')


@router.post('/products', response_model=BaseResponse)
async def collect_data(
    data: BaseRequest,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    return await request.app.state.service.collect_data(data.artikul, session)


@router.get('/subscribe/{artikul}', response_model=ResponseMessage)
async def subscribe(artikul: int, request: Request):
    return await request.app.state.service.subscribe(artikul)


@router.delete('/subscribe/{artikul}', response_model=ResponseMessage)
async def unsubscribe(
    artikul: int,
    request: Request,
):
    return await request.app.state.service.unsubscribe(artikul)


@router.get('/products/{artikul}', response_model=BaseResponse)
async def get_product(artikul: int, request: Request):
    return await request.app.state.service.get_product(artikul)
