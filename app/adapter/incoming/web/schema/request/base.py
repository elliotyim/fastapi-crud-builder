from fastapi import Query
from pydantic import BaseModel


class RequestList(BaseModel):
    page: int = 1
    per_page: int = 20
    filter_conditions: list[str] = []
    sort_conditions: list[str] = []

    @classmethod
    def as_param(
        cls,
        page: int = Query(default=1, description="<h3>Page number (1-index)</h3>"),
        per_page: int = Query(default=20, description="<h3>Items per page</h3>"),
        filter_conditions: list[str] = Query(
            default=[],
            description="<h3>Filter conditions</h3>"
            "<p>Supported operator: <code>==</code>, <code>!=</code>, <code><=</code>, <code>>=</code>, <code><</code>, <code>></code>, <code>like</code>, <code>ilike</code>, <code>in</code></p>"
            'Value must be one of these type: number, string, bool, list; ex) <code>1</code>, <code>"32"</code>, <code>true</code>, <code>[1,2,3]</code>'
            '<p>ex) [<code>"id::>::1"</code>, <code>name::like::"Jake"</code>, <code>author.name::in::["Jake"]</code>]</p>',
        ),
        sort_conditions: list[str] = Query(
            default=[],
            description="<h3>Sort conditions</h3>"
            "<p>Supported operator: <code>asc</code>, <code>desc</code></p>"
            '<p>ex) [<code>"name::desc"</code>, <code>"author.name::asc"</code>]</p>',
        ),
    ):
        if page < 1:
            raise ValueError("page must be positive number.")
        elif page < 1:
            raise ValueError("page must be positive number.")
        elif page > 100:
            page = 20

        return cls(
            page=page,
            per_page=per_page,
            filter_conditions=filter_conditions,
            sort_conditions=sort_conditions,
        )
