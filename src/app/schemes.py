from datetime import datetime

from pydantic import BaseModel, Field


class BaseRequest(BaseModel):
    artikul: int


class BaseResponseCheck(BaseRequest):
    name: str
    rating: int | float
    price: int = Field(alias='priceU')
    sale_price: int = Field(alias='salePriceU')
    total_quantity: int = Field(alias='totalQuantity')
    review_rating: float = Field(alias='reviewRating')


class BaseResponse(BaseResponseCheck):
    id: int
    price: int
    sale_price: int
    total_quantity: int
    review_rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True


class ResponseMessage(BaseModel):
    message: str
