from .utils import assert_status_and_return_data


def test_list_parties(client):
    data = assert_status_and_return_data(client.get, "/api/party/", status_code=200)

    # will change when we add resource scoping with respect to the request JWT
    assert len(data) == 2
    party = data[0]
    assert party == {"id": 1, "name": "Famille McTrickfoot"}


def test_describe_party(client):
    data = assert_status_and_return_data(client.get, "/api/party/1", status_code=200)
    assert data["id"] == 1
    assert data["name"] == "Famille McTrickfoot"
    assert len(data["members"]) == 4


def test_describe_party_without_players(client):
    data = assert_status_and_return_data(client.get, "/api/party/2", status_code=200)
    assert data["id"] == 2
    assert data["name"] == "La Compagnie des Gourmands"
    assert len(data["members"]) == 0


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


def test_update_party_invalid_body(client):
    update_response = client.put(
        "/api/party/1",
        json={"name": "McTrickfoot Family", "invalid": "field"},
    )
    assert update_response.status_code == 422
