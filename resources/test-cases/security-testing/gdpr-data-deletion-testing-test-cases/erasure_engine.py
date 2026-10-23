"""Minimal GDPR Article 17 erasure engine on stdlib sqlite3.

Models a TaskFlow-like system: a primary user store, related tables,
a search-index table, a cache table, application logs, marketing
segments, a third-party outbox, an audit trail, legal holds and a
backup/restore mechanism with tombstone replay.

Everything is synchronous and in-memory by default so the pytest
suite exercises the propagation rules without external services.
"""

import sqlite3
import time

PII_TABLES = (
    ("users", "email"),
    ("orders", "email"),
    ("search_index", "doc"),
    ("cache", "value"),
    ("app_logs", "line"),
)


class ErasureEngine:
    """Article-17 erasure flow: verify, hold-check, propagate, audit."""

    def __init__(self, db_path=":memory:"):
        self.db = sqlite3.connect(db_path)
        self.db.row_factory = sqlite3.Row
        self._create_schema()
        self.processors = []
        self.outbox = []
        self.tombstones = set()

    def _create_schema(self):
        self.db.executescript(
            """
            CREATE TABLE users (
                id TEXT PRIMARY KEY, email TEXT, name TEXT,
                zip TEXT, birth_year INTEGER, marketing_consent INTEGER DEFAULT 0);
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT,
                email TEXT, name TEXT, zip TEXT, birth_year INTEGER, amount REAL);
            CREATE TABLE sessions (id TEXT PRIMARY KEY, user_id TEXT);
            CREATE TABLE search_index (doc_id TEXT PRIMARY KEY, user_id TEXT, doc TEXT);
            CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT);
            CREATE TABLE app_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, line TEXT);
            CREATE TABLE marketing_segments (user_id TEXT, segment TEXT);
            CREATE TABLE audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL,
                request_id TEXT, user_id TEXT, action TEXT, scope TEXT, status TEXT);
            CREATE TABLE legal_holds (user_id TEXT PRIMARY KEY, reason TEXT);
            """
        )
        self.db.commit()

    # ------------------------------------------------------------------
    # Seeding helpers
    # ------------------------------------------------------------------
    def seed_user(self, user_id="u-4821", email="qa-erasure-01@taskflow.test",
                  name="QA Erasure", zip="08001", birth_year=1990, orders=5):
        self.db.execute(
            "INSERT INTO users (id,email,name,zip,birth_year,marketing_consent)"
            " VALUES (?,?,?,?,?,1)",
            (user_id, email, name, zip, birth_year),
        )
        for _ in range(orders):
            self.db.execute(
                "INSERT INTO orders (user_id,email,name,zip,birth_year,amount)"
                " VALUES (?,?,?,?,?,?)",
                (user_id, email, name, zip, birth_year, 49.99),
            )
        self.db.execute("INSERT INTO sessions VALUES (?,?)", ("sess-1", user_id))
        self.db.execute(
            "INSERT INTO search_index VALUES (?,?,?)",
            ("doc-1", user_id, f"{name} {email}"),
        )
        self.db.execute(
            "INSERT INTO cache VALUES (?,?)",
            (f"user:{user_id}", f'{{"email":"{email}"}}'),
        )
        self.db.execute(
            "INSERT INTO app_logs (line) VALUES (?)",
            (f"login user_id={user_id} email={email}",),
        )
        self.db.execute(
            "INSERT INTO marketing_segments VALUES (?,?)", (user_id, "seg-news")
        )
        self.db.commit()

    # ------------------------------------------------------------------
    # Erasure flow
    # ------------------------------------------------------------------
    def request_erasure(self, user_id, verified=True,
                        request_id="dsar-2026-0142", now=None):
        """Entry point. Returns rejected / deferred / noop / fulfilled."""
        now = time.time() if now is None else now
        if not verified:
            self._audit(now, request_id, user_id, "erasure", "none", "rejected")
            return {"status": "rejected"}
        if self.db.execute(
            "SELECT 1 FROM legal_holds WHERE user_id=?", (user_id,)
        ).fetchone():
            self._audit(now, request_id, user_id, "erasure", "none", "deferred")
            return {"status": "deferred"}
        if not self.db.execute(
            "SELECT 1 FROM users WHERE id=?", (user_id,)
        ).fetchone():
            # unknown or already deleted: idempotent no-op
            return {"status": "noop"}
        return self._erase_row(user_id, now, request_id)

    def _erase_row(self, user_id, now, request_id):
        email = self.db.execute(
            "SELECT email FROM users WHERE id=?", (user_id,)
        ).fetchone()["email"]
        scope = []

        self.db.execute("DELETE FROM users WHERE id=?", (user_id,))
        scope.append("users")
        # orders keep the amount; every identifier is dropped
        self.db.execute(
            "UPDATE orders SET email=NULL, name=NULL, zip=NULL, birth_year=NULL"
            " WHERE user_id=?",
            (user_id,),
        )
        scope.append("orders")
        self.db.execute("DELETE FROM sessions WHERE user_id=?", (user_id,))
        scope.append("sessions")
        self.db.execute("DELETE FROM search_index WHERE user_id=?", (user_id,))
        scope.append("search_index")
        self.db.execute("DELETE FROM cache WHERE key=?", (f"user:{user_id}",))
        scope.append("cache")
        self.db.execute(
            "UPDATE app_logs SET line = replace(replace(line, ?, '[redacted]'),"
            " ?, '[redacted]')",
            (user_id, email),
        )
        scope.append("app_logs")
        self.db.execute(
            "DELETE FROM marketing_segments WHERE user_id=?", (user_id,)
        )
        scope.append("marketing_segments")

        self.tombstones.add(user_id)
        self._notify_processors(user_id)
        self._audit(now, request_id, user_id, "erasure", ",".join(scope), "fulfilled")
        self.db.commit()
        return {"status": "fulfilled", "scope": scope}

    def _notify_processors(self, user_id):
        for processor in self.processors:
            self.outbox.append(
                {"processor": processor, "user_id": user_id, "status": "sent"}
            )

    def confirm_processors(self):
        for message in self.outbox:
            message["status"] = "confirmed"

    # ------------------------------------------------------------------
    # Legal hold (Art. 17(3))
    # ------------------------------------------------------------------
    def add_legal_hold(self, user_id, reason="pending litigation"):
        self.db.execute(
            "INSERT INTO legal_holds VALUES (?,?)", (user_id, reason)
        )
        self.db.commit()

    def release_legal_hold(self, user_id):
        self.db.execute("DELETE FROM legal_holds WHERE user_id=?", (user_id,))
        self.db.commit()

    # ------------------------------------------------------------------
    # Backup / restore with tombstone replay
    # ------------------------------------------------------------------
    def snapshot(self):
        return {
            table: self.db.execute(f"SELECT * FROM {table}").fetchall()
            for table in ("users", "orders", "sessions", "search_index",
                          "cache", "app_logs", "marketing_segments")
        }

    def restore(self, snap):
        for table, rows in snap.items():
            self.db.execute(f"DELETE FROM {table}")
            for row in rows:
                cols = row.keys()
                self.db.execute(
                    f"INSERT INTO {table} ({','.join(cols)})"
                    f" VALUES ({','.join('?' * len(cols))})",
                    tuple(row),
                )
        self.db.commit()
        self.replay_tombstones()

    def replay_tombstones(self):
        for user_id in list(self.tombstones):
            if self.db.execute(
                "SELECT 1 FROM users WHERE id=?", (user_id,)
            ).fetchone():
                self._erase_row(user_id, time.time(), "tombstone-replay")

    # ------------------------------------------------------------------
    # Consent withdrawal (Art. 17(1)(b))
    # ------------------------------------------------------------------
    def withdraw_consent(self, user_id):
        self.db.execute(
            "UPDATE users SET marketing_consent=0 WHERE id=?", (user_id,)
        )
        removed = self.db.execute(
            "DELETE FROM marketing_segments WHERE user_id=?", (user_id,)
        ).rowcount
        self.db.commit()
        return removed

    # ------------------------------------------------------------------
    # Export and verification helpers
    # ------------------------------------------------------------------
    def generate_export(self):
        rows = self.db.execute(
            "SELECT id, email, name FROM users ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]

    def pii_residue(self, needle):
        """Count rows still containing the needle across the PII map."""
        hits = 0
        for table, column in PII_TABLES:
            hits += self.db.execute(
                f"SELECT COUNT(*) AS c FROM {table} WHERE {column} LIKE ?",
                (f"%{needle}%",),
            ).fetchone()["c"]
        return hits

    def reidentify(self, user_id):
        """Identifier columns still present in retained order rows."""
        return self.db.execute(
            "SELECT COUNT(*) AS c FROM orders WHERE user_id=? AND"
            " (email IS NOT NULL OR name IS NOT NULL OR zip IS NOT NULL"
            " OR birth_year IS NOT NULL)",
            (user_id,),
        ).fetchone()["c"]

    def audit_entries(self, user_id):
        return self.db.execute(
            "SELECT * FROM audit_log WHERE user_id=? ORDER BY id", (user_id,)
        ).fetchall()

    def confirmation_for(self, request_id):
        row = self.db.execute(
            "SELECT * FROM audit_log WHERE request_id=? AND status='fulfilled'",
            (request_id,),
        ).fetchone()
        if row is None:
            return None
        return {
            "request_id": row["request_id"],
            "scope": row["scope"].split(","),
            "completed_at": row["ts"],
        }

    def _audit(self, ts, request_id, user_id, action, scope, status):
        self.db.execute(
            "INSERT INTO audit_log (ts,request_id,user_id,action,scope,status)"
            " VALUES (?,?,?,?,?,?)",
            (ts, request_id, user_id, action, scope, status),
        )
        self.db.commit()
