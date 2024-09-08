from pydantic import BaseModel


class PaginationMixin(BaseModel):
    total: int
    total_page: int
    prev_page: int | None = None
    next_page: int | None = None

    class Config:
        from_attributes = True
