from __future__ import annotations

from abc import ABC, abstractmethod


class Ledger(ABC):

    __slots__ = ()

    @property
    @abstractmethod
    def balance(self) -> int:
        """The total balance of the ledger at this time."""

    @abstractmethod
    def deposit(self, amount: int) -> str:
        """Deposit the amount in ledger and return the transaction ID.

        Args:
            amount: The money amount to be deposited.
        Returns:
            The unique ID for the deposit transaction.
        Raises:
            ValueError if the amount is not positive.
        """

    @abstractmethod
    def withdraw(self, amount: int) -> str:
        """Withdraw the amount from the ledger and return the transaction ID.

        Args:
            amount: The money amount to be withdrawn.

        Returns:
            The unique ID for the withdrawal transaction.

        Raises:
            ValueError if the amount is not positive.
        """
