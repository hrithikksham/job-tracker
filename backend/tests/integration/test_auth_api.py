import uuid
import random

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_user():

    return {
        "name": "Test User",
        "email": f"{uuid.uuid4().hex}@gmail.com",
        "phone_number": str(
            random.randint(
                9000000000,
                9999999999
            )
        ),
        "password": "Password123"
    }


def test_register_user():

    user = create_test_user()

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["success"] is True
    assert "user_id" in data


def test_duplicate_email():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    duplicate_user = {
        "name": "Duplicate User",
        "email": user["email"],
        "phone_number": str(
            random.randint(
                9000000000,
                9999999999
            )
        ),
        "password": "Password123"
    }

    response = client.post(
        "/auth/register",
        json=duplicate_user
    )

    assert response.status_code == 400


def test_duplicate_phone_number():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    duplicate_user = {
        "name": "Duplicate User",
        "email": f"{uuid.uuid4().hex}@gmail.com",
        "phone_number": user["phone_number"],
        "password": "Password123"
    }

    response = client.post(
        "/auth/register",
        json=duplicate_user
    )

    assert response.status_code == 400


def test_login_with_email():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    response = client.post(
        "/auth/login",
        json={
            "identifier": user["email"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_with_phone_number():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    response = client.post(
        "/auth/login",
        json={
            "identifier": user["phone_number"],
            "password": user["password"]
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data
    assert "refresh_token" in data


def test_invalid_password():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    response = client.post(
        "/auth/login",
        json={
            "identifier": user["email"],
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


def test_refresh_token():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "identifier": user["email"],
            "password": user["password"]
        }
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()[
        "refresh_token"
    ]

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "access_token" in data


def test_get_profile():

    user = create_test_user()

    register = client.post(
        "/auth/register",
        json=user
    )

    assert register.status_code == 200

    login_response = client.post(
        "/auth/login",
        json={
            "identifier": user["email"],
            "password": user["password"]
        }
    )

    assert login_response.status_code == 200

    access_token = login_response.json()[
        "access_token"
    ]

    response = client.get(
        "/profile",
        headers={
            "Authorization":
            f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True


def test_profile_without_token():

    response = client.get(
        "/profile"
    )

    assert response.status_code in [401, 403]