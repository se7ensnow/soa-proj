def test_register_user_success(client):
    payload = {
        "username": "testuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_register_duplicate_username(client):
    first_payload = {
        "username": "testuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    first_response = client.post("/auth/register", json=first_payload)
    assert first_response.status_code == 200

    copy_payload = {
        "username": "testuser",
        "password": "AnotherPass!",
        "email": "new@example.com"
    }
    response = client.post("/auth/register", json=copy_payload)
    assert response.status_code == 400
    assert "Username taken" in response.text

def test_register_invalid_email(client):
    payload = {
        "username": "bademail",
        "password": "Test1234!",
        "email": "not-an-email"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text

def test_login_success(client):
    reg_payload = {
        "username": "testuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    reg_response = client.post("/auth/register", json=reg_payload)
    assert reg_response.status_code == 200

    login_payload = {
        "username": "testuser",
        "password": "StrongPass123!"
    }
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "user_id" in data

def test_login_wrong_password(client):
    reg_payload = {
        "username": "testuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    reg_response = client.post("/auth/register", json=reg_payload)
    assert reg_response.status_code == 200

    payload = {
        "username": "testuser",
        "password": "WrongPassword!"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 400
    assert "Incorrect password" in response.text

def test_login_wrong_username(client):
    reg_payload = {
        "username": "testuser",
        "password": "StrongPass123!",
        "email": "test@example.com",
    }
    reg_response = client.post("/auth/register", json=reg_payload)
    assert reg_response.status_code == 200

    payload = {
        "username": "wronguser",
        "password": "StrongPass123!"
    }
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 404
    assert "User not found" in response.text