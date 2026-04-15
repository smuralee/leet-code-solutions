class LedgerError(Exception):
    """Raised for all ledger operation errors."""


class EntryNotFoundError(LedgerError, KeyError):
    """Raised when the transaction ID is not found for the ledger operations."""


class TransactionError(LedgerError, RuntimeError):
    """Raised when the transaction operations e.g. commit/rollback without an active transaction."""
