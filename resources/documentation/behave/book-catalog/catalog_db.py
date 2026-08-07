# catalog_db.py
import sqlite3
from collections import namedtuple
from typing import List, Optional


Book = namedtuple('Book', ['title', 'available'])


class CatalogDB:
    """A catalog backed by a sqlite3 connection and cursor.

    The caller is responsible for transaction boundaries. This class only
    executes DML so that `environment.py` can roll back each scenario with a
    savepoint. Pass an existing connection for the test suite, or call with no
    arguments to spin up a runnable `:memory:` catalog.
    """

    def __init__(
        self,
        connection: Optional[sqlite3.Connection] = None,
        connection_string: str = ':memory:',
    ):
        if connection is None:
            self.connection = sqlite3.connect(connection_string)
            self._ensure_table()
        else:
            self.connection = connection
        self.cursor = self.connection.cursor()

    def _ensure_table(self):
        self.connection.execute(
            'CREATE TABLE IF NOT EXISTS books ('
            'title TEXT PRIMARY KEY, '
            'available INTEGER NOT NULL'
            ')'
        )

    def add(self, title: str, available: bool = True):
        self.cursor.execute(
            'INSERT INTO books (title, available) VALUES (?, ?)',
            (title, int(available)),
        )

    def search(self, title: str) -> List[Book]:
        self.cursor.execute(
            'SELECT title, available FROM books WHERE title = ?', (title,)
        )
        return [
            Book(title=row[0], available=bool(row[1]))
            for row in self.cursor.fetchall()
        ]
