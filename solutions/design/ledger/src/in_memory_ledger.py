from __future__ import annotations
import uuid
from .ledger import Ledger
from typing import NamedTuple, Callable


class _Entry(NamedTuple):
    id: str
    amount: int


class _ThreadState:
    """
    Per-thread transaction state.

    Each thread gets it's own pending entries list and savepoints, so that
    concurrent transactions do not interfere with each other.
    """

    __slots__ = "entries"

    def __init__(self):
        self.entries: list[_Entry] = []


def _generate_txn_id() -> str:
    return f"txn-{uuid.uuid4()}"


class InMemoryLedger(Ledger):

    def __init__(self, *, id_factory: Callable[[], str] = _generate_txn_id) -> None:
        raise NotImplementedError("Unsupported operation")
