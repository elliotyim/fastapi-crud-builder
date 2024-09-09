from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    class Config:
        from_attributes = True


class PaginationMixin(BaseModel):
    total: int
    total_page: int
    prev_page: int | None = None
    next_page: int | None = None
