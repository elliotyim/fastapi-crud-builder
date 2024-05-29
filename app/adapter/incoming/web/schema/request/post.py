from pydantic import BaseModel


class RequestPostCreate(BaseModel):
    title: str
    content: str
    author_id: str


class RequestPostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
