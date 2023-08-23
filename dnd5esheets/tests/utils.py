from fastapi.testclient import TestClient

from dnd5esheets import ExtendedFastAPI


def assert_status_and_return_data(client_method, url, status_code, *args, **kwargs):
    response = client_method(url, *args, **kwargs)
    assert (
        response.status_code == status_code
    ), f"Expected: {status_code}, got: {response.status_code}"
    return response.json()


def log_as(email: str, app: ExtendedFastAPI) -> TestClient:
    _client = TestClient(app)
    _client.post("/api/login/token", data={"username": email, "password": "azerty"})
    return _client
