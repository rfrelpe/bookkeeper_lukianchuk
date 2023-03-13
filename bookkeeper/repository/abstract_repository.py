"""
Repository protocol class module.

This may be short-cited, but to arguably reduce coupling (and to test myself) I swithced
from double inheritance from ABC and Generic[T] to a generic Protocol of T.

An object which follows the protocol would implement entry storage, which assigns
a unique primary key (pk) to each entry. Objects to be stored should implement
the pk attribute and should not use it otherwise.
"""

from abc import abstractmethod
from typing import TypeVar, Protocol, Any, runtime_checkable


class KeyObject(Protocol):  # pylint: disable=too-few-public-methods
    """
    An object that has a primary key attribute.
    """

    pk: int


T = TypeVar("T", bound=KeyObject)


@runtime_checkable
class RepositoryProtocol(Protocol[T]):
    """
    Repository protocol
    Methods:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Add an object to the repo and return its id.
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:
        """
        Get and object with a fixed id.
        """

    @abstractmethod
    def get_all_where(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Get all entries that satisfy all "where" conditions, return all
        entris if where is None.
        where is a dictionary {"entry_field": value}
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """
        Update an entry with the same pk as the object.
        """

    @abstractmethod
    def delete(self, pk: int) -> None:
        """
        Remove an entry.
        """
