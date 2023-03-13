"""
Budget class tests.
"""
from bookkeeper.models.budget import Budget

def test_create_with_full_args_list():
    """
    The class should be correctly initialised.
    """
    bgt = Budget(
        amount=100,
        period="day",
        pk=1,
    )
    assert bgt.amount == 100
    assert bgt.period == "day"
    assert bgt.get_spent() == 0


def test_can_add_expense():
    """
    The class should correctly update spent value.
    """
    bgt = Budget(1000, "day")
    bgt.count_in(100)
    assert bgt.get_spent() == 100
    bgt.count_in(200)
    assert bgt.get_spent() == 300
