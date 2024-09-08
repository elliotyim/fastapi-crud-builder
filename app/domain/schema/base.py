from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, model_validator

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


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 20

    @model_validator(mode="before")
    @classmethod
    def validate(cls, data: any) -> any:
        if "page" in data and data["page"] < 1:
            raise ValueError("page must be positive number.")
        elif "per_page" in data:
            if data["per_page"] < 1:
                raise ValueError("page must be positive number.")
            elif data["per_page"] > 100:
                data["per_page"] = 100

        return data

    class Config:
        from_attributes = True


class PaginatedList(Generic[T], BaseModel):
    total: int
    total_page: int
    prev_page: int | None = None
    next_page: int | None = None

    items: list = []
