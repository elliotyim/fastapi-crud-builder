from pydantic import BaseModel

from app.domain.schema.base import CreateSchema, UpdateSchema


class User(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True


class UserCreate(CreateSchema):
    name: str


class UserUpdate(UpdateSchema):
    name: str | None
