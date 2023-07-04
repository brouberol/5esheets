from jose import jwt

from .utils import assert_status_and_return_data


def test_login(unauthed_client, settings):
    response = unauthed_client.post(
        "/api/login/token", data={"username": "br@test.com", "password": "azerty"}
    )
    assert response.status_code == 200
    # assert "set-cookie" in response.headers
    # assert response.headers["set-cookie"].startswith('Authorization="Bearer ')
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    plaintext_jwt = jwt.decode(
        token=data["access_token"],
        key=settings.SECRET_KEY,
        algorithms=[settings.JWT_ENCODING_ALGORITHM],
    )
    assert plaintext_jwt["sub"] == "br@test.com"
    assert "exp" in plaintext_jwt
    assert "Authorization" in unauthed_client.cookies


def test_login_no_credentials(client):
    assert_status_and_return_data(
        client.post,
        "/api/login/token",
        status_code=422,
    )


def test_login_wrong_credentials(client):
    data = assert_status_and_return_data(
        client.post,
        "/api/login/token",
        status_code=401,
        data={"username": "br@test.com", "password": "WRONG PASSWORD"},
    )
    assert data == {"detail": "Incorrect username or password"}
