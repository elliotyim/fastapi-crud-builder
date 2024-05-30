from fastapi import Body
from pydantic import BaseModel


class RequestPostCreate(BaseModel):
    title: str = Body(..., description="Post Title")
    content: str = Body(..., description="Post Content")
    author_id: str = Body(..., description="Author ID")


class RequestPostUpdate(BaseModel):
    title: str | None = Body(None, description="Post Title")
    content: str | None = Body(None, description="Post Content")
