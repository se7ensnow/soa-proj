import pytest
from fastapi.testclient import TestClient

from api_gateway_app.main import app

@pytest.fixture(scope="function")
def api_client():
    with TestClient(app) as client:
        yield client