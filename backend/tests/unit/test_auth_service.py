from unittest.mock import AsyncMock, patch

import pytest

from app.services.auth_service import AuthService
from app.schemas.user import UserRegister
from app.schemas.user import UserLogin
from app.utils.password import hash_password



@patch("app.services.auth_service.UserRepository")
async def test_register_success(mock_repo):

    mock_repo.find_by_email = AsyncMock(
        return_value=None
    )

    mock_repo.find_by_phone_number = AsyncMock(
        return_value=None
    )

    mock_repo.create = AsyncMock()

    data = UserRegister(
        name="Hrithik",
        email="hrithik@test.com",
        phone_number="9876543210",
        password="Password123"
    )

    user = await AuthService.register(data)

    assert user["email"] == "hrithik@test.com"



@patch("app.services.auth_service.UserRepository")
async def test_register_duplicate_email(
    mock_repo
):

    mock_repo.find_by_email = AsyncMock(
        return_value={
            "email": "hrithik@test.com"
        }
    )

    data = UserRegister(
        name="Hrithik",
        email="hrithik@test.com",
        phone_number="9876543210",
        password="Password123"
    )

    with pytest.raises(Exception):

        await AuthService.register(
            data
        )

@patch("app.services.auth_service.UserRepository")
async def test_login_success(
    mock_repo
):

    password = "Password123"

    mock_repo.find_by_identifier = AsyncMock(
        return_value={
            "_id": "user123",
            "email": "hrithik@test.com",
            "password_hash": hash_password(
                password
            )
        }
    )

    mock_repo.update_refresh_token = AsyncMock()

    data = UserLogin(
        identifier="hrithik@test.com",
        password=password
    )

    result = await AuthService.login(
        data
    )

    assert "access_token" in result

    assert "refresh_token" in result

@patch("app.services.auth_service.UserRepository")
async def test_login_invalid_password(
    mock_repo
):

    mock_repo.find_by_identifier = AsyncMock(
        return_value={
            "_id": "user123",
            "password_hash": hash_password(
                "correct-password"
            )
        }
    )

    data = UserLogin(
        identifier="hrithik@test.com",
        password="wrong-password"
    )

    with pytest.raises(Exception):

        await AuthService.login(
            data
        )

@patch("app.services.auth_service.UserRepository")
async def test_login_user_not_found(
    mock_repo
):

    mock_repo.find_by_identifier = AsyncMock(
        return_value=None
    )

    data = UserLogin(
        identifier="unknown@test.com",
        password="Password123"
    )

    with pytest.raises(Exception):

        await AuthService.login(
            data
        )