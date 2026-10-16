-- Schema for transaction testing demos (SQLite)
-- Invariants: balances are never negative; version increments on every write
-- (optimistic-locking pattern).

PRAGMA foreign_keys = ON;

CREATE TABLE accounts (
    id      INTEGER PRIMARY KEY,
    owner   TEXT NOT NULL,
    balance INTEGER NOT NULL CHECK (balance >= 0),
    version INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE transfers (
    id         INTEGER PRIMARY KEY,
    from_id    INTEGER NOT NULL REFERENCES accounts(id),
    to_id      INTEGER NOT NULL REFERENCES accounts(id),
    amount     INTEGER NOT NULL CHECK (amount > 0),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
