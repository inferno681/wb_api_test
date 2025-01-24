from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.constants import NAME_LENGTH
from app.db.basemodels import Base

datetime_field = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP,
        server_default=func.now(),
    ),
]


class Product(Base):
    """Product model."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_LENGTH))
    artikul: Mapped[int] = mapped_column(Integer, unique=True)
    rating: Mapped[int]
    price: Mapped[int]
    sale_price: Mapped[int]
    total_quantity: Mapped[int]
    review_rating: Mapped[float] = mapped_column(Numeric(2, 1))
    created_at: Mapped[datetime_field]
    updated_at: Mapped[datetime_field]
