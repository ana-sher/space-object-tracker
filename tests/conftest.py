from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine

from application.api import app
from tracker.models import Base


@pytest.fixture(scope="function")
def test_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def client(test_engine) -> Generator[TestClient, None, None]:
    from adapters.database_storage import load_satellites, load_space_objects

    app.dependency_overrides = {}

    original_load_satellites = load_satellites
    original_load_space_objects = load_space_objects

    def load_satellites_override(_, page, limit):
        return original_load_satellites(test_engine, page, limit)

    def load_space_objects_override(_, page, limit):
        return original_load_space_objects(test_engine, page, limit)

    app.dependency_overrides[load_satellites] = load_satellites_override
    app.dependency_overrides[load_space_objects] = load_space_objects_override

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
