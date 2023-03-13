"""
Expense class tests.
"""
from datetime import datetime

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.expense import Expense


@pytest.fixture(name="repo")
def fixture_repository():
    """
    A fixture to text repository integration of the class.
    """
    return MemoryRepository()


def test_create_with_full_args_list():
    """
    The class should be correctly initialised.
    """
    exp = Expense(
        amount=100,
        category=1,
        expense_date=datetime.now(),
        comment="test",
        pk=1,
    )
    assert exp.amount == 100
    assert exp.category == 1


def test_create_brief():
    """
    The class should be correctly initialised.
    """
    exp = Expense(100, 1)
    assert exp.amount == 100
    assert exp.category == 1


def test_can_add_to_repo(repo):
    """
    A repository should have no trouble adding an instance of the class.
    """
    e = Expense(100, 1)
    pk = repo.add(e)
    assert e.pk == pk
