"""
A module for a repository that works from RAM.
"""

from itertools import count
from typing import Generic, Any


from bookkeeper.repository.abstract_repository import T


class MemoryRepository(Generic[T]):
    """
    RAM repository, stores data in a dictionary.
    """

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        """
        Add an object to the repo and return its id.
        """
        if getattr(obj, "pk", None) != 0:
            raise ValueError(
                f'trying to add an object {obj} with a filled "pk" attribute'
            )
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        """
        Get and object with a fixed id.
        """
        return self._container.get(pk)

    def get_all_where(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Get all entries that satisfy all "where" conditions, return all
        entris if where is None.
        where is a dictionary {"entry_field": value}
        """
        if where is None:
            return list(self._container.values())
        return [
            obj
            for obj in self._container.values()
            if all(getattr(obj, attr) == value for attr, value in where.items())
        ]

    def update(self, obj: T) -> None:
        """
        Update an entry with the same pk as the object.
        """
        if obj.pk == 0:
            raise ValueError("trying to update an object with an unknown primary key")
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        """
        Remove an entry.
        """
        self._container.pop(pk)
