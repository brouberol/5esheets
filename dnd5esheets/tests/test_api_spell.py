from .utils import assert_status_and_return_data


def test_get_spell(client):
    data = assert_status_and_return_data(client.get, "/api/spell/1", status_code=200)

    assert data["name"] == "Blade of Disaster"


def test_get_spell_etag(client):
    response = client.get("/api/spell/1")
    assert "etag" in response.headers
