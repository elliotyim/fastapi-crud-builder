import json

from sqlalchemy import Select, func, inspect, select
from sqlalchemy.orm import InstrumentedAttribute, Session, joinedload

from app.domain.entity import Base
from app.domain.schema.base import (
    C,
    CreateSchema,
    K,
    OrderBy,
    PaginatedList,
    Pagination,
    T,
    U,
    UpdateSchema,
    Where,
)
from app.port.outbound.repository.base import CRUDRepositoryPort


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

    def _validate_fields(self, fields: list[str]) -> None:
        target = self._entity
        for i, field in enumerate(fields):
            if not hasattr(target, field):
                raise ValueError(f"{'.'.join(fields)} is not valid")
            if i < len(fields) - 1:
                target = getattr(target, field).property.mapper.class_

    def _extract_fields(self, field: str) -> list[InstrumentedAttribute]:
        result = []
        target = self._entity
        fields = field.split(".")

        self._validate_fields(fields)

        for f in fields[:-1]:
            field = getattr(target, f)
            result.append(field)
            target = field.property.mapper.class_

        result.append(getattr(target, fields[-1]))
        return result

    def _select(self) -> Select:
        return select(self._entity)

    def _filter(self, query: Select, where: list[Where]) -> Select:
        for w in where:
            fields = self._extract_fields(w.field)

            for field in fields[:-1]:
                query = query.join(field)

            column = fields[-1]
            value = json.loads(w.value)

            match w.operator:
                case "==":
                    query = query.filter(column == value)
                case "!=":
                    query = query.filter(column != value)
                case "<":
                    query = query.filter(column < value)
                case ">":
                    query = query.filter(column > value)
                case "<=":
                    query = query.filter(column <= value)
                case ">=":
                    query = query.filter(column >= value)
                case "like":
                    query = query.filter(column.like(f"%{value}%"))
                case "ilike":
                    query = query.filter(column.ilike(f"%{value}%"))
                case "in":
                    query = query.filter(column.in_(value))

        return query

    def _sort(self, query: Select, order_by: list[OrderBy]) -> Select:
        for o in order_by:
            fields = self._extract_fields(o.field)

            for field in fields[:-1]:
                query = query.join(field)

            column = fields[-1]
            query = query.order_by(column.asc() if o.order == "asc" else column.desc())

        return query

    def _eager_load(self, query: Select, eager_loading_fields: list[str]) -> Select:
        # TODO: Implement eager loading for all nested fields
        if eager_loading_fields:
            joined_fields = [
                joinedload(getattr(self._entity, field))
                for field in eager_loading_fields
            ]
            query = query.options(*joined_fields)
        return query

    def _execute(self, query: Select, page: int, per_page: int) -> PaginatedList:
        total = self._db.execute(
            select(func.count()).select_from(query.subquery())
        ).scalar()
        total_page = total // per_page + (1 if total % per_page else 0)
        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if total_page > page else None

        entities = self._db.execute(query).unique().scalars().all()
        result = PaginatedList(
            items=entities,
            total=total,
            total_page=total_page,
            prev_page=prev_page,
            next_page=next_page,
        )
        return result

    def find_all(
        self,
        where: list[Where] | None = None,
        order_by: list[OrderBy] | None = None,
        pagination: Pagination | None = None,
        eager_loading_fields: list[str] = None,
        **kwargs,
    ) -> PaginatedList:
        where = [] if where is None else where
        order_by = [] if order_by is None else order_by
        pagination = Pagination() if pagination is None else pagination
        eager_loading_fields = (
            [] if eager_loading_fields is None else eager_loading_fields
        )

        query = self._select()
        query = self._filter(query, where)
        query = self._sort(query, order_by)
        query = self._eager_load(query, eager_loading_fields)

        result = self._execute(
            query=query, page=pagination.page, per_page=pagination.per_page
        )
        return result

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
