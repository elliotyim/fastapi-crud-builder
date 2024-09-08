from fastapi import Body
from pydantic import BaseModel


class RequestUserCreate(BaseModel):
    name: str = Body(..., description="User Name")


class RequestUserUpdate(BaseModel):
    name: str | None = Body(None, description="User Name")
