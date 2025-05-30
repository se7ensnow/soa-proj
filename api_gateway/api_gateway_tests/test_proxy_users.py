def test_register_user_success(api_client):
    payload = {
        "username": "proxyuser",
        "email": "proxy@example.com",
        "password": "Test1234!"
    }

    response = api_client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "proxyuser"
    assert data["email"] == "proxy@example.com"

def test_register_user_missing_body(api_client):
    response = api_client.post("/auth/register")
    assert response.status_code == 400
    assert "Missing or invalid JSON body" in response.text

def test_register_user_invalid_email(api_client):
    payload = {
        "username": "invalidemail",
        "email": "notanemail",
        "password": "StrongPass123!"
    }
    response = api_client.post("/auth/register", json=payload)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text

def test_register_user_duplicate_username(api_client):
    payload = {
        "username": "dupeuser",
        "email": "dupe1@example.com",
        "password": "StrongPass123!"
    }
    first = api_client.post("/auth/register", json=payload)
    assert first.status_code == 200

    payload["email"] = "dupe2@example.com"
    second = api_client.post("/auth/register", json=payload)
    assert second.status_code == 400
    assert "Username taken" in second.text

def test_login_user_success(api_client):
    payload = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "StrongPass123!"
    }
    reg = api_client.post("/auth/register", json=payload)
    assert reg.status_code == 200

    login_data = {
        "username": payload["username"],
        "password": payload["password"]
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = api_client.post("/auth/login", data=login_data, headers=headers)
    assert response.status_code == 200
    token = response.json().get("access_token")
    assert token is not None

def test_login_user_invalid_password(api_client):
    payload = {
        "username": "badloginuser",
        "email": "badlogin@example.com",
        "password": "CorrectPass123!"
    }
    reg = api_client.post("/auth/register", json=payload)
    assert reg.status_code == 200

    bad_login = {
        "username": payload["username"],
        "password": "WrongPassword"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = api_client.post("/auth/login", data=bad_login, headers=headers)
    assert response.status_code == 401
    assert "Incorrect password" in response.text

def register_and_login(api_client, username, email="test@example.com", password="Test1234!"):
    reg_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    reg_response = api_client.post("/auth/register", json=reg_payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    login_data = {
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    login_response = api_client.post("/auth/login", data=login_data, headers=headers)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return user_id, token

def test_get_user_profile(api_client):
    user_id, token = register_and_login(api_client, "profileuser", "profile@example.com")
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "profileuser"
    assert data["email"] == "profile@example.com"

def test_get_user_invalid_id(api_client):
    response = api_client.get("/users/999999")
    assert response.status_code == 404
    assert "User not found" in response.text

def test_update_user_profile_success(api_client):
    user_id, token = register_and_login(api_client, "updateuser", "update@example.com")

    update_payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "birth_date": "1992-05-12",
        "email": "updated@example.com",
        "phone_number": "+12345678901"
    }

    response = api_client.put("/users/update", json=update_payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["email"] == "updated@example.com"

def test_update_user_invalid_email(api_client):
    _, token = register_and_login(api_client, "bademailuser", "bademail@example.com")

    update_payload = {
        "email": "not-an-email"
    }

    response = api_client.put("/users/update", json=update_payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text

def test_update_user_invalid_phone(api_client):
    _, token = register_and_login(api_client, "badphoneuser", "badphone@example.com")

    update_payload = {
        "phone_number": "invalidphone"
    }

    response = api_client.put("/users/update", json=update_payload, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 422
    assert "Invalid phone number" in response.text

def test_update_user_unauthorized(api_client):
    update_payload = {
        "first_name": "Hacker"
    }
    response = api_client.put("/users/update", json=update_payload)
    assert response.status_code == 401
    assert "Missing Authorization header" in response.text