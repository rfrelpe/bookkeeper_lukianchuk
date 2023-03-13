"""
Repository protocol class tests.
"""

from bookkeeper.repository.abstract_repository import RepositoryProtocol
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository


def test_repos_implement():
    """
    Repositories must implement the protocol correctly.
    """
    assert issubclass(MemoryRepository, RepositoryProtocol)
    assert issubclass(SQLiteRepository, RepositoryProtocol)
