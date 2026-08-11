import pytest


@pytest.fixture
def state():
    return {"catalog": {}, "cart": {}, "discount": 0.0}
