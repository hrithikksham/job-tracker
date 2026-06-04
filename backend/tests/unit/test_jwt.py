from app.utils.jwt import (
    create_access_token,
    verify_token
)

def test_access_token_creation():

    token = create_access_token(
        "user123"
    )

    payload = verify_token(
        token
    )

    assert payload["sub"] == "user123"