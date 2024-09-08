from datetime import datetime

from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self):
        _id = f"{self.id}" if hasattr(self, "id") else None
        return f"<{self.__class__} id={_id}>"
