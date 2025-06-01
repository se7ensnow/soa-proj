import pytest
from fastapi.testclient import TestClient
from user_service_app.database import Base, engine
from user_service_app.main import app

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True, scope='function')
def clean_db():
    connection = engine.connect()
    transaction = connection.begin()

    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(table.delete())

    transaction.commit()
    connection.close()