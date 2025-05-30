import pytest
import psycopg2
import os
from fastapi.testclient import TestClient

from api_gateway_app.main import app

USER_DATABASE_URL = os.getenv("USER_SERVICE_TEST_DATABASE_URL")
POST_DATABASE_URL = os.getenv("POST_SERVICE_TEST_DATABASE_URL")

@pytest.fixture(scope="session", autouse=True)
def clean_users_table():
    conn = psycopg2.connect(USER_DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")
    finally:
        cur.close()
        conn.close()

    yield

# @pytest.fixture(scope="session", autouse=True)
# def clean_posts_table():
#     conn = psycopg2.connect(POST_DATABASE_URL)
#     conn.autocommit = True
#     cur = conn.cursor()
#
#     try:
#         cur.execute("TRUNCATE TABLE posts RESTART IDENTITY CASCADE;")
#     finally:
#         cur.close()
#         conn.close()
#
#     yield


@pytest.fixture(scope="session")
def api_client():
    with TestClient(app) as client:
        yield client