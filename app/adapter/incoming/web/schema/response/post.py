from pydantic import BaseModel

from app.adapter.incoming.web.schema.response.base import PaginationMixin
from app.adapter.incoming.web.schema.response.user import ResponseUser


class ResponsePost(BaseModel):
    id: int
    title: str
    content: str | None = None

    author: ResponseUser

    class Config:
        from_attributes = True


class ResponsePostList(PaginationMixin, BaseModel):
    items: list[ResponsePost]

    class Config:
        from_attributes = True
