from app.utils.password import (
    hash_password,
    verify_password
)

def test_hash_password():
    password = "Password123"

    hashed = hash_password(password)

    assert hashed != password

def test_verify_password():
    password = "Password123"

    hashed = hash_password(password)

    assert verify_password(
        password,
        hashed
    )