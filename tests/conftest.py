import pytest
from fastapi.testclient import TestClient
from typing import Generator
from sentinel_events.main import app
from sentinel_events import store


@pytest.fixture(autouse=True)
def clear_store() -> Generator[None, None, None]:
    store.d.clear()
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
