from app.services.seed_service import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify_round_trip():
    password_hash = hash_password("secret123")

    assert verify_password("secret123", password_hash)
    assert not verify_password("wrong-password", password_hash)


def test_access_token_round_trip():
    token = create_access_token(42, "mentor")

    payload = decode_access_token(token)

    assert payload["sub"] == "42"
    assert payload["role"] == "mentor"
