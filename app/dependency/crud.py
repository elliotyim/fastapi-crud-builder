from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependency.db import get_db
from app.domain.entity import Base
from app.domain.schema.base import CreateSchema, UpdateSchema
from app.domain.service.crud import CRUDService, CRUDServiceBuilder


def crud_service_factory(
    entity: type[Base],
    create_schema: type[CreateSchema],
    update_schema: type[UpdateSchema],
) -> Callable[[Session], CRUDService]:
    def build_service(db: Session = Depends(get_db)) -> CRUDService:
        return (
            CRUDServiceBuilder()
            .set_entity(entity)
            .set_create_schema(create_schema)
            .set_update_schema(update_schema)
            .set_session(db)
            .build()
        )

    return build_service
