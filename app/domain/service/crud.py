from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.adapter.outbound.crud import GenericCRUDRepositoryAdapter
from app.domain.entity import Base
from app.domain.schema.base import (
    CreateSchema,
    K,
    OrderBy,
    PaginatedList,
    Pagination,
    T,
    UpdateSchema,
    Where,
)
from app.port.outbound.repository.base import CRUDRepositoryPort


class CRUDService:
    def __init__(self, entity: type[Base], crud_repository: CRUDRepositoryPort):
        self._entity = entity
        self._crud_repository = crud_repository

    def retrieve(self, pk: K) -> T:
        instance = self._crud_repository.find_by_id(pk)
        if not instance:
            raise NoResultFound()
        return instance

    def retrieve_all(
        self,
        filter_conditions: list[str] | None = None,
        sort_conditions: list[str] | None = None,
        pagination: Pagination | None = None,
        eager_loading_fields: list[str] = None,
        **kwargs,
    ) -> PaginatedList:
        where = []
        for f in filter_conditions:
            value = f.split("::")
            where.append(Where(field=value[0], operator=value[1], value=value[2]))

        order_by = []
        for s in sort_conditions:
            value = s.split("::")
            order_by.append(OrderBy(field=value[0], order=value[1]))

        result = self._crud_repository.find_all(
            where=where,
            order_by=order_by,
            pagination=pagination,
            eager_loading_fields=eager_loading_fields,
        )
        return result

    def create(self, create_schema: CreateSchema) -> T:
        instance = self._crud_repository.create(create_schema)
        self._crud_repository.add(instance)
        self._crud_repository.commit()
        return instance

    def put(self, pk: K, update_schema: UpdateSchema) -> T:
        instance = self.retrieve(pk)
        self._crud_repository.update_all(instance, update_schema)
        self._crud_repository.commit()
        return instance

    def patch(self, pk: K, update_schema: UpdateSchema) -> T:
        instance = self.retrieve(pk)
        self._crud_repository.update(instance, update_schema)
        self._crud_repository.commit()
        return instance

    def delete(self, pk: K) -> None:
        instance = self.retrieve(pk)
        self._crud_repository.delete(instance)
        self._crud_repository.commit()


class CRUDServiceBuilder:
    entity: type[Base]
    session: Session
    create_schema: type[CreateSchema]
    update_schema: type[UpdateSchema]

    def set_entity(self, entity: type[Base]) -> "CRUDServiceBuilder":
        self.entity = entity
        return self

    def set_create_schema(
        self, create_schema: type[CreateSchema]
    ) -> "CRUDServiceBuilder":
        self.create_schema = create_schema
        return self

    def set_update_schema(
        self, update_schema: type[UpdateSchema]
    ) -> "CRUDServiceBuilder":
        self.update_schema = update_schema
        return self

    def set_session(self, session: Session) -> "CRUDServiceBuilder":
        self.session = session
        return self

    def build(self) -> CRUDService:
        if self.entity is None:
            raise NotImplementedError("entity is not defined")
        elif not issubclass(self.entity, Base):
            raise ValueError("entity must be a subclass of Base")
        elif self.create_schema is None:
            raise NotImplementedError("create_schema is not defined")
        elif self.create_schema is None:
            raise NotImplementedError("update_schema is not defined")

        crud_repository = GenericCRUDRepositoryAdapter(
            db=self.session,
            entity=self.entity,
            create_schema=self.create_schema,
            update_schema=self.update_schema,
        )

        return CRUDService(entity=self.entity, crud_repository=crud_repository)
