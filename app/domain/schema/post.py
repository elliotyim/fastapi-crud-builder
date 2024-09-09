from app.domain.schema.base import CreateSchema, UpdateSchema


class PostCreate(CreateSchema):
    title: str
    content: str
    author_id: str


class PostUpdate(UpdateSchema):
    title: str | None = None
    content: str | None = None


class PostCommentCreate(CreateSchema):
    author_id: str
    post_id: int
    content: str


class PostCommentUpdate(UpdateSchema):
    content: str | None = None
