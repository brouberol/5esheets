import pytest

from .utils import assert_status_and_return_data


def test_list_parties(client):
    data = assert_status_and_return_data(client.get, "/api/party/", status_code=200)

    assert len(data) == 1
    party = data[0]
    assert party == {"id": 1, "name": "Famille McTrickfoot"}


def test_describe_party(client):
    data = assert_status_and_return_data(client.get, "/api/party/1", status_code=200)
    assert data["id"] == 1
    assert data["name"] == "Famille McTrickfoot"
    assert len(data["members"]) == 4


@pytest.mark.parametrize(
    "client_fixture_name, status_code",
    [
        ("mctrickfoot_family_player", 200),  # player
        ("mctrickfoot_family_gm", 200),  # gm
        ("compagnie_des_gourmands_player", 403),  # outsider
    ],
)
def test_describe_party_security_policy(client_fixture_name, status_code, request):
    client = request.getfixturevalue(f"client_as_{client_fixture_name}")
    assert_status_and_return_data(
        client.get,
        f"/api/party/1",
        status_code=status_code,
    )


def test_update_party(client):
    data = assert_status_and_return_data(client.get, "/api/party/1", status_code=200)
    assert data["name"] == "Famille McTrickfoot"
    assert_status_and_return_data(
        client.put,
        "/api/party/1",
        json={"name": "McTrickfoot Family"},
        status_code=200,
    )
    data = assert_status_and_return_data(client.get, "/api/party/1", status_code=200)
    assert data["name"] == "McTrickfoot Family"


@pytest.mark.parametrize(
    "client_fixture_name, status_code",
    [
        ("mctrickfoot_family_player", 403),  # player
        ("mctrickfoot_family_gm", 200),  # gm
        ("compagnie_des_gourmands_player", 403),  # outsider
    ],
)
def test_describe_party_security_policy(client_fixture_name, status_code, request):
    client = request.getfixturevalue(f"client_as_{client_fixture_name}")
    assert_status_and_return_data(
        client.put,
        f"/api/party/1",
        status_code=status_code,
        json={"name": "Le Clan des Semi-Croustillants"},
    )


def test_update_party_invalid_body(client):
    update_response = client.put(
        "/api/party/1",
        json={"name": "McTrickfoot Family", "invalid": "field"},
    )
    assert update_response.status_code == 422
