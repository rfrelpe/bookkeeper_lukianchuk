"""
Memory repository class tests.
"""

from bookkeeper.repository.memory_repository import MemoryRepository

import pytest


@pytest.fixture(name="custom_class")
def fixture_custom_class():
    """
    A fixture of a model of a class for repo.
    """

    class Custom:
        pk = 0

    return Custom


@pytest.fixture(name="repo")
def fixture_repository():
    """
    A fixture to text repository integration of the class.
    """
    return MemoryRepository()


def test_crud(repo, custom_class):
    """
    All CRUD operations should be performed correctly.
    """
    # create
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    # read
    assert repo.get(pk) == obj
    # update
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    # delete
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    """
    An object can't have a pk when being added.
    """
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    """
    An object must have a pk attribute to be added.
    """
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    """
    One cannot delete something that isn't there.
    """
    with pytest.raises(KeyError):
        repo.delete(1)


def test_cannot_update_without_pk(repo, custom_class):
    """
    An object must have a pk when being a template for an update.
    """
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    """
    Getting entries of the repo should work correctly.
    """
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all_where() == objects


def test_get_all_with_condition(repo, custom_class):
    """
    Getting entries of the repo should work correctly.
    """
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        o.test = "test"
        repo.add(o)
        objects.append(o)
    assert repo.get_all_where({"name": "0"}) == [objects[0]]
    assert repo.get_all_where({"test": "test"}) == objects
