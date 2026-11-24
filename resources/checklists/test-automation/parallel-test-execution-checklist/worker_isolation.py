"""Worker-scoped isolation helpers for pytest-xdist.

Every worker gets a unique ID (gw0, gw1, ...) exposed as
PYTEST_XDIST_WORKER. Use it to namespace shared resources:
database schemas, port ranges, temp directories, test users.

Usage in conftest.py:

    from worker_isolation import worker_schema, worker_db_url

    @pytest.fixture(scope="session")
    def db_engine(worker_id):
        create_schema(worker_schema(worker_id))
        yield create_engine(worker_db_url(worker_id))
        drop_schema(worker_schema(worker_id))
"""

import os

DEFAULT_BASE_PORT = 10000
PORTS_PER_WORKER = 100


def worker_id() -> str:
    """Return the xdist worker name, or 'master' for serial runs."""
    return os.environ.get("PYTEST_XDIST_WORKER", "master")


def worker_index() -> int:
    """Numeric index: gw0 -> 0, gw3 -> 3, master (serial) -> 0."""
    wid = worker_id()
    if wid.startswith("gw"):
        return int(wid[2:])
    return 0


def worker_schema(wid: str | None = None) -> str:
    """Database schema name unique to this worker, e.g. 'test_gw2'."""
    return f"test_{wid or worker_id()}"


def worker_db_url(wid: str | None = None, base_url: str | None = None) -> str:
    """Postgres URL pointing at the worker's own schema."""
    base = base_url or os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432"
    )
    return f"{base}/{worker_schema(wid)}"


def worker_port_range() -> range:
    """A 100-port block unique to this worker for services that bind ports."""
    start = DEFAULT_BASE_PORT + worker_index() * PORTS_PER_WORKER
    return range(start, start + PORTS_PER_WORKER)


def test_user(role: str = "user") -> str:
    """Unique username per worker to avoid collisions on shared accounts."""
    return f"{role}_{worker_id()}_{os.getpid()}"
