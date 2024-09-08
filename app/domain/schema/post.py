from pydantic import BaseModel

from app.domain.schema.base import CreateSchema, UpdateSchema
from app.domain.schema.user import User


class Post(BaseModel):
    id: int
    title: str
    content: str | None = None

    author: User

    class Config:
        from_attributes = True


class PostCreate(CreateSchema):
    title: str
    content: str
    author_id: str


class PostUpdate(UpdateSchema):
    title: str | None = None
    content: str | None = None
