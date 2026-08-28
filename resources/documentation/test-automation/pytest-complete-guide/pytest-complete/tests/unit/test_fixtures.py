import pytest


def test_admin_user(make_user):
    admin = make_user(email="admin@example.com", role="admin")
    assert admin["role"] == "admin"


def test_reader_user(make_user):
    reader = make_user()
    assert reader["role"] == "reader"


@pytest.mark.parametrize("backend", ["redis", "memcached"])
def test_cache_backend_set_get(backend):
    class FakeCache:
        def __init__(self):
            self._store = {}

        def set(self, key, value):
            self._store[key] = value

        def get(self, key):
            return self._store.get(key)

    cache = FakeCache()
    cache.set("key", "value")
    assert cache.get("key") == "value"


@pytest.mark.slow
def test_temp_file_content(temp_file):
    assert temp_file.read_text() == "test content"
