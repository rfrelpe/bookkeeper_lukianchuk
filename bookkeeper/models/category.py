"""
Category class module.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from bookkeeper.repository.abstract_repository import RepositoryProtocol


@dataclass
class Category:
    """
    Expense category, stores the expense name and the parent category's id.
    For a top-level Category parent is None.
    """

    name: str
    parent: int | None = None
    pk: int = 0

    def get_parent(self, repo: RepositoryProtocol["Category"]) -> "Category | None":
        """
        Get a parents Category.
        For a top-level Category returns None.

        Parameters
        ----------
        repo - repository to get objects from.

        Returns
        -------
        Parent Category or None.
        """
        if self.parent is None:
            return None
        return repo.get(self.parent)

    def get_all_parents(
        self, repo: RepositoryProtocol["Category"]
    ) -> Iterator["Category"]:
        """
        Get all Categories up the hierarchy.

        Parameters
        ----------
        repo - repository to get objects from.

        Yields
        -------
        Parent Category objects and higher.
        """
        parent = self.get_parent(repo)
        if parent is None:
            return
        yield parent
        yield from parent.get_all_parents(repo)

    def get_subcategories(
        self, repo: RepositoryProtocol["Category"]
    ) -> Iterator["Category"]:
        """
        Get all subcategories of the hierarchy, i.e. all subcategories of
        this one, all their subcategories etc.

        Parameters
        ----------
        repo - repository to get objects from.

        Yields
        -------
        Category type objects, that are different level subcategories of this one.
        """

        def get_children(
            graph: dict[int | None, list["Category"]], root: int
        ) -> Iterator["Category"]:
            """DFS of the graph from the root."""
            for x in graph[root]:
                yield x
                yield from get_children(graph, x.pk)

        subcats = defaultdict(list)
        for cat in repo.get_all_where():
            subcats[cat.parent].append(cat)
        return get_children(subcats, self.pk)

    @classmethod
    def create_from_tree(
        cls, tree: list[tuple[str, str | None]], repo: RepositoryProtocol["Category"]
    ) -> list["Category"]:
        """
        Create a tree of (child-parent) pairs of Caterogies.

        The tree is topologically sorted, i.e. children are placed after their parents.
        Data correctness isn't checked. For a DBMS with foreign key checks an exeption
        is raised (IntergrityError for sqlite3). For a DBMS with no checks the end
        result could be correct if the initial data is correct except for sorting, and
        couldn't otherwise, "garbage in, garbage out".

        Parameters
        ----------
        tree - list of (child-parent) pair.
        repo - repository to store the objects.

        Returns
        -------
        List of the created Category objects.
        """
        created: dict[str, Category] = {}
        for child, parent in tree:
            cat = cls(child, created[parent].pk if parent is not None else None)
            repo.add(cat)
            created[child] = cat
        return list(created.values())
