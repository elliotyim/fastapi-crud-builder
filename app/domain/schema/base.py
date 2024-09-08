from typing import Literal, TypeVar

from pydantic import BaseModel

from app.domain.entity import Base


class CreateSchema(BaseModel):
    class Config:
        from_attributes = True


class UpdateSchema(BaseModel):
    class Config:
        from_attributes = True


K = TypeVar("K", bound=int | str)  # ID Key
T = TypeVar("T", bound=Base)  # Entity Type
C = TypeVar("C", bound=CreateSchema)  # Create Schema
U = TypeVar("U", bound=UpdateSchema)  # Update Schema


class Where(BaseModel):
    field: str
    operator: Literal["==", "!=", "<", ">", "<=", ">=", "like", "ilike", "in"]
    value: int | str | bool

    class Config:
        from_attributes = True


class OrderBy(BaseModel):
    field: str
    order: Literal["asc", "desc"]

    class Config:
        from_attributes = True


class PaginatedList(BaseModel):
    total: int
    total_page: int
    prev_page: int | None = None
    next_page: int | None = None

    items: list = []
