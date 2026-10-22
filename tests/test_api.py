def test_register_user_returns_user_details(client):
    response = client.post(
        "/user-register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["username"] == "testuser"
    assert body["email"] == "test@example.com"
    assert body["role"] == "employee"
    assert "id" in body
    assert "hashed_password" not in body


def test_register_user_rejects_duplicate_username(client):
    user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "secret123",
    }
    first_response = client.post("/user-register", json=user)
    second_response = client.post(
        "/user-register",
        json={
            "username": "testuser",
            "email": "another@example.com",
            "password": "secret456",
        },
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Username or email already registered"


def test_register_user_rejects_invalid_payload(client):
    response = client.post(
        "/user-register",
        json={"username": "ab", "email": "test@example.com", "password": "short"},
    )

    assert response.status_code == 422


def test_login_rejects_unknown_user(client):
    response = client.post(
        "/user/login",
        data={"username": "missing", "password": "secret123"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_employees_requires_authentication(client):
    response = client.get("/employees")

    assert response.status_code == 401
