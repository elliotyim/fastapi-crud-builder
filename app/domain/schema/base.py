from pydantic import BaseModel


class CreateSchema(BaseModel):
    class Config:
        from_attributes = True


class UpdateSchema(BaseModel):
    class Config:
        from_attributes = True
