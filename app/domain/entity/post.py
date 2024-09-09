from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    author_id: Mapped[str] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship("User", back_populates="posts", uselist=False)
    comments: Mapped[list["PostComment"]] = relationship(
        "PostComment",
        back_populates="post",
        cascade="all, delete-orphan",
        uselist=True,
    )


class PostComment(Base):
    __tablename__ = "post_comment"

    id: Mapped[int] = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        autoincrement=True,
    )
    content: Mapped[str] = Column(Text, nullable=True)

    author_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    author: Mapped["User"] = relationship(
        "User", back_populates="comments", uselist=False
    )
    post: Mapped["Post"] = relationship(
        "Post", back_populates="comments", uselist=False
    )
