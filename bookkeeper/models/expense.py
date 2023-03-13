"""
Expense class module.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Expense operation.

    amount - expense sum
    category - expense Category id
    expense_date - the date that expense happened
    comment - additional info on the expense
    pk - id for the repo
    """

    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    comment: str = ""
    pk: int = 0
