from app.adapter.incoming.web.schema.response.base import BaseModel, PaginationMixin
from app.adapter.incoming.web.schema.response.user import ResponseUser


class ResponsePostComment(BaseModel):
    id: int
    content: str

    author: ResponseUser


class ResponsePost(BaseModel):
    id: int
    title: str
    content: str | None = None

    author: ResponseUser
    comments: list[ResponsePostComment] = []


class ResponsePostList(PaginationMixin, BaseModel):
    items: list[ResponsePost]


class ResponsePostCommentList(PaginationMixin, BaseModel):
    items: list[ResponsePostComment]
