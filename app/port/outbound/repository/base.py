import abc
from typing import Generic, TypeVar

from pydantic import BaseModel

from app.domain.entity import Base

K = TypeVar("K", bound=int | str)  # ID Key
T = TypeVar("T", bound=Base)  # Entity Type
C = TypeVar("C", bound=BaseModel)  # Create Schema
U = TypeVar("U", bound=BaseModel)  # Update Schema


class CRUDRepositoryPort(abc.ABC, Generic[K, T, C, U]):
    @abc.abstractmethod
    def find_by_id(self, id_key: K) -> T:
        """
        Get entity by ID key

        Args:
            id_key (K): Primary key

        Returns:
            T: Entity
        """
        pass

    @abc.abstractmethod
    def create(self, create_schema: C) -> T:
        """
        Create an entity

        Args:
            create_schema (C): Required properties of the entity

        Returns:
            T: Entity
        """
        pass

    @abc.abstractmethod
    def update(self, entity: T, update_schema: U) -> T:
        """
        Update the entity partially.
        Any property set None, won't be changed.

        Args:
            entity (T): Target entity
            update_schema (U): Properties will be changed

        Returns:
            T: Entity
        """
        pass

    @abc.abstractmethod
    def update_all(self, entity: T, update_schema: U) -> T:
        """
        Update the whole properties of the entity.
        Any property set None, it will be set as None.

        Args:
            entity (T): Target entity
            update_schema (U): Properties will be changed

        Returns:
            T: Entity
        """
        pass

    @abc.abstractmethod
    def delete(self, entity: T) -> None:
        """
        Delete the entity

        Args:
             entity (T): Target entity

        Returns:
            None
        """
        pass

    @abc.abstractmethod
    def add(self, entity: T) -> T:
        """
        Place an object into the ORM Session

        Args:
            entity (T): Target entity

        Returns:
            T: Entity
        """
        pass

    @abc.abstractmethod
    def add_all(self, entities: list[T]) -> list[T]:
        """
        Place objects into the ORM Session

        Args:
            entities (list[T]): Target entities

        Returns:
            list[T]: Entities
        """
        pass

    @abc.abstractmethod
    def flush(self) -> None:
        """
        Flush all the changes to the database.
        """
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        """
        Commit all the changes to the database.
        """
        pass
