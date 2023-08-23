import pytest

from .utils import assert_status_and_return_data


def test_describe_player(client):
    data = assert_status_and_return_data(client.get, "/api/player/1", status_code=200)
    assert data["id"] == 1
    assert data["name"] == "Balthazar"
    assert len(data["characters"]) == 1  # Douglas


@pytest.mark.parametrize(
    "client_fixture_name, status_code",
    [
        ("mctrickfoot_family_gm", 200),  # owner
        ("mctrickfoot_family_player", 403),  # non owner
    ],
)
def test_describe_player_security_policy(client_fixture_name, status_code, request):
    client = request.getfixturevalue(f"client_as_{client_fixture_name}")
    assert_status_and_return_data(
        client.get,
        "/api/player/1",
        status_code=status_code,
    )


def test_update_player(client):
    data = assert_status_and_return_data(client.get, "/api/player/1", status_code=200)
    assert data["name"] == "Balthazar"
    assert_status_and_return_data(
        client.put,
        "/api/player/1",
        json={"name": "Ronald"},
        status_code=200,
    )
    data = assert_status_and_return_data(client.get, "/api/player/1", status_code=200)
    assert data["name"] == "Ronald"


@pytest.mark.parametrize(
    "client_fixture_name, status_code",
    [
        ("mctrickfoot_family_gm", 200),  # owner
        ("mctrickfoot_family_player", 403),  # non owner
    ],
)
def test_update_player_security_policy(client_fixture_name, status_code, request):
    client = request.getfixturevalue(f"client_as_{client_fixture_name}")
    assert_status_and_return_data(
        client.put, "/api/player/1", status_code=status_code, json={"name": "Gauvain"}
    )


def test_update_player_invalid_body(client):
    update_response = client.put(
        "/api/player/1",
        json={"name": "Ronald", "invalid": "field"},
    )
    assert update_response.status_code == 422
