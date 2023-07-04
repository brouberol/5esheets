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
