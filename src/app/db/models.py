from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column


from app.db.basemodels import Base


class Product(Base):
    """Product model."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    artikul: Mapped[int] = mapped_column(Integer, unique=True)
    rating: Mapped[int]
    priceU: Mapped[int]
    salePriceU: Mapped[int]
    totalQuantity: Mapped[int]
    reviewRating: Mapped[float] = mapped_column(Numeric(2, 1))
