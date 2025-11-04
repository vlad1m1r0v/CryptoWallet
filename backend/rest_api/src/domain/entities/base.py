from typing import Any, TypeVar

from src.domain.exceptions.base import DomainException

from src.domain.value_objects.base import ValueObject

T = TypeVar("T", bound=ValueObject)


class EntityCannotBeInstantiatedDirectlyException(DomainException):
    message = "Entity can't be instantiated directly."


class ChangingEntityIdIsNotPermittedException(DomainException):
    message = "Changing entity ID is not permitted."


class Entity[T: ValueObject]:
    """
    raises DomainException

    Base class for domain entities, defined by a unique identity (`id`).
    - `id`: Identity that remains constant throughout the entity's lifecycle.
    - Entities are mutable, but are compared solely by their `id`.
    """

    def __init__(self, *, id_: T) -> None:
        """:raises DomainException:"""
        self.__forbid_base_class_instantiation()
        self.id_ = id_

    def __forbid_base_class_instantiation(self) -> None:
        """:raises DomainException:"""
        if type(self) is Entity:
            raise EntityCannotBeInstantiatedDirectlyException()

    def __setattr__(self, name: str, value: Any) -> None:
        """
        :raises DomainException:

        Prevents modifying the `id` after it's set.
        Other attributes can be changed as usual.
        """
        if name == "id_" and getattr(self, "id_", None) is not None:
            raise ChangingEntityIdIsNotPermittedException()
        super().__setattr__(name, value)

    def __eq__(self, other: Any) -> bool:
        """
        Two entities are considered equal if they have the same `id`,
        regardless of other attribute values.
        """
        return type(self) is type(other) and other.id_ == self.id_

    def __hash__(self) -> int:
        """
        Generate a hash based on entity type and the immutable `id`.
        This allows entities to be used in hash-based collections and
        reduces the risk of hash collisions between different entity types.
        """
        return hash((type(self), self.id_))
