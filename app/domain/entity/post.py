from sqlalchemy import BigInteger, Column, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.domain.entity import Base


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = Column(String(100), index=True, nullable=False)
    content: Mapped[str] = Column(Text, nullable=True)

    author: Mapped["User"] = relationship("User", back_populates="posts", uselist=False)
