def test_proxy_register(api_client):
    payload = {
        "username": "proxyuser",
        "password": "Test1234!",
        "email": "proxy@example.com"
    }

    response = api_client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "proxyuser"
    assert data["email"] == "proxy@example.com"

def test_proxy_login(api_client):
    reg_payload = {
        "username": "proxyuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    reg_response = api_client.post("/auth/login", json=reg_payload)
    assert reg_response.status_code == 200

    login_payload = {
        "username": "proxyuser",
        "password": "StrongPass123!"
    }
    response = api_client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "user_id" in data

def test_proxy_get_user(api_client):
    reg_payload = {
        "username": "proxyuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    reg_response = api_client.post("/auth/register", json=reg_payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "proxyuser"
    assert data["email"] == "test@example.com"

def test_proxy_update_user(api_client):
    payload = {
        "username": "proxyuser",
        "password": "Test1234!",
        "email": "proxy@example.com"
    }
    reg_response = api_client.post("/auth/register", json=payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    update_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "birth_date": "1999-02-02",
        "email": "new_proxy@example.com",
        "phone_number": "+74951234567"
    }
    response = api_client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["first_name"] == "John"
    assert data["last_name"] == "Smith"
    assert data["birth_date"] == "1999-02-02"
    assert data["email"] == "new_proxy@example.com"
    assert data["phone_number"] == "+74951234567"

def test_proxy_user_not_found(api_client):
    user_id = 123456
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert "User not found" in response.text