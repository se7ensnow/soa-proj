import pytest
import uuid

@pytest.fixture
def auth_headers(api_client):
    username = f"postuser_{uuid.uuid4().hex[:8]}"
    email = f"{username}@example.com"

    payload = {
        "username": username,
        "email": email,
        "password": "StrongPass123!"
    }
    reg = api_client.post("/auth/register", json=payload)
    assert reg.status_code == 200

    login_data = {
        "username": username,
        "password": "StrongPass123!"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login = api_client.post("/auth/login", data=login_data, headers=headers)
    assert login.status_code == 200

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_post(api_client, auth_headers):
    payload = {
        "title": "Gateway Post",
        "description": "Created via API Gateway",
        "is_private": False,
        "tags": ["tag1", "tag2"]
    }

    response = api_client.post("/posts/create", json=payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["is_private"] == payload["is_private"]
    assert data["tags"] == payload["tags"]

    return int(data["id"])

def test_update_post(api_client, auth_headers):
    post_id = test_create_post(api_client, auth_headers)

    update_payload = {
        "title": "Updated Post",
        "description": "Updated via API Gateway",
        "is_private": True,
        "tags": ["updated", "post"]
    }

    response = api_client.put(f"/posts/update/{post_id}", json=update_payload, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_payload["title"]
    assert data["description"] == update_payload["description"]
    assert data["is_private"] == update_payload["is_private"]
    assert data["tags"] == update_payload["tags"]

def test_delete_post(api_client, auth_headers):
    post_id = test_create_post(api_client, auth_headers)

    response = api_client.delete(f"/posts/delete/{post_id}", headers=auth_headers)
    assert response.status_code == 200

    get_response = api_client.get(f"/posts/{post_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_list_posts(api_client, auth_headers):
    for i in range(3):
        payload = {
            "title": f"Post {i}",
            "description": f"Description {i}",
            "is_private": False,
            "tags": [f"tag{i}"]
        }
        api_client.post("/posts/create", json=payload, headers=auth_headers)

    response = api_client.get("/posts/list", params={"page": 1, "size": 10}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "posts" in data
    assert "total" in data
    assert data["total"] >= 3