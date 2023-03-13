from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Budget for a certain category of expensese for a certain period of time.
    Not fully implemented.

    period - time period in dats
    amount - total sum
    spent - already spent money
    """

    amount: float
    period: str
    _spent: float = 0
    pk: int = 0

    def count_in(self, exp: float):
        """
        Take a new expense into account.
        """
        self._spent += exp

    def get_spent(self) -> float:
        """
        Getter for the spent attribute.
        """
        return self._spent
