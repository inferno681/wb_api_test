from enum import Enum

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Abstract base class for tables in db."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        """Table names from class names."""
        return cls.__name__.lower()

    def to_dict(self):
        """Model to dict."""
        return {
            field.name: (
                getattr(self, field.name).value
                if isinstance(getattr(self, field.name), Enum)
                else getattr(self, field.name)
            )
            for field in self.__table__.c
        }
