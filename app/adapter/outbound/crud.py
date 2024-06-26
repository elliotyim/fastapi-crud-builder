from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.domain.entity import Base
from app.domain.schema.base import CreateSchema, UpdateSchema
from app.port.outbound.repository.base import C, CRUDRepositoryPort, K, T, U


class GenericCRUDRepositoryAdapter(CRUDRepositoryPort[K, T, C, U]):
    def __init__(
        self,
        db: Session,
        entity: type[Base],
        create_schema: type[CreateSchema],
        update_schema: type[UpdateSchema],
    ):
        self._db = db
        self._entity = entity
        self._create_schema = create_schema
        self._update_schema = update_schema

    def find_by_id(self, id_key: K) -> T:
        id_field = inspect(self._entity).primary_key[0].name
        return self._db.execute(
            select(self._entity).where(getattr(self._entity, id_field) == id_key)
        ).scalar()

    def create(self, create_schema: C) -> T:
        return self._entity(**create_schema.model_dump(mode="json"))

    def update(self, entity: T, update_schema: U) -> T:
        for k, v in update_schema.model_dump(mode="json").items():
            if v is not None and hasattr(entity, k):
                setattr(entity, k, v)
        return entity

    def update_all(self, entity: T, update_schema: U) -> T:
        for k, v in update_schema.model_dump(mode="json").items():
            if hasattr(entity, k):
                setattr(entity, k, v)
        return entity

    def delete(self, entity: T) -> None:
        self._db.delete(entity)

    def add(self, entity: T) -> T:
        self._db.add(entity)
        self._db.flush()
        return entity

    def add_all(self, entities: list[T]) -> list[T]:
        self._db.add_all(entities)
        self._db.flush()
        return entities

    def flush(self) -> None:
        self._db.flush()

    def commit(self) -> None:
        self._db.commit()
