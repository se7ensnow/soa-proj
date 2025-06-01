def test_update_user_profile(client):
    payload = {
        "username": "profileuser",
        "password": "Test1234!",
        "email": "profile@example.com"
    }
    reg_response = client.post("/auth/register", json=payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    update_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "birth_date": "1999-02-02",
        "email": "new_profile@example.com",
        "phone_number": "+74951234567"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["first_name"] == "John"
    assert data["last_name"] == "Smith"
    assert data["birth_date"] == "1999-02-02"
    assert data["email"] == "new_profile@example.com"
    assert data["phone_number"] == "+74951234567"

def test_update_user_invalid_email(client):
    payload = {
        "username": "bademailuser",
        "password": "Test1234!",
        "email": "valid@example.com"
    }
    reg_response = client.post("/auth/register", json=payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    update_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "birth_date": "1999-02-02",
        "email": "not_an_email",
        "phone_number": "+79161234567"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 422
    assert "value is not a valid email address" in response.text

def test_update_user_invalid_phone(client):
    payload = {
        "username": "badphoneuser",
        "password": "Test1234!",
        "email": "badphone@example.com"
    }
    reg_response = client.post("/auth/register", json=payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    update_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "birth_date": "1999-02-02",
        "email": "badphone@example.com",
        "phone_number": "invalid_phone"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 422
    assert "Invalid phone number" in response.text

def test_update_user_invalid_id(client):
    user_id = 123456
    update_payload = {
        "first_name": "John",
        "last_name": "Smith",
        "birth_date": "1999-02-02",
        "email": "badid@example.com",
        "phone_number": "+79161234567"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 404
    assert "User not found" in response.text

def test_get_user_profile(client):
    payload = {
        "username": "profileuser",
        "password": "Test1234!",
        "email": "profile@example.com"
    }
    reg_response = client.post("/auth/register", json=payload)
    assert reg_response.status_code == 200
    user_id = reg_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "profileuser"
    assert data["email"] == "profile@example.com"

def test_get_user_invalid_id(client):
    user_id = 123456
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert "User not found" in response.text