from dnd5esheets.api.login import AuthJWT

from .utils import assert_status_and_return_data


def test_login(unauthed_client):
    response = unauthed_client.post(
        "/api/login/token", data={"username": "br@test.com", "password": "azerty"}
    )
    assert response.status_code == 200
    assert "set-cookie" in response.headers
    assert response.headers["set-cookie"].startswith("access_token_cookie=")
    assert "access_token_cookie" in unauthed_client.cookies


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
