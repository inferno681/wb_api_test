from pydantic import BaseModel


class BaseRequest(BaseModel):
    artikul: int


class BaseResponseCheck(BaseModel):
    name: str
    artikul: int
    rating: int | float
    priceU: int
    salePriceU: int
    totalQuantity: int
    reviewRating: float
