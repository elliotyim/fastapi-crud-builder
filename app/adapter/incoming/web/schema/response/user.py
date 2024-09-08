from pydantic import BaseModel

from app.adapter.incoming.web.schema.response.base import PaginationMixin


class ResponseUser(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class ResponseUserList(PaginationMixin, BaseModel):
    items: list[ResponseUser]

    class Config:
        from_attributes = True
