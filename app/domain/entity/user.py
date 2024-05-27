import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship

from app.domain.entity import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = Column(String(200), nullable=False, index=True)

    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="author", cascade="all, delete-orphan", uselist=True
    )
