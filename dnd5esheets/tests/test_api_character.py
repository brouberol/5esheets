from .utils import assert_status_and_return_data


def test_list_characters(client):
    data = assert_status_and_return_data(client.get, "/api/character/", status_code=200)

    assert len(data) == 1

    assert data[0] == {
        "class_": "Artilleur",
        "id": 1,
        "level": 4,
        "name": "Douglas McTrickfoot",
        "party": {"id": 1, "name": "Famille McTrickfoot"},
        "player": {"id": 1, "name": "Balthazar"},
        "slug": "douglas-mctrickfoot",
    }


def test_describe_character(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert "equipment" in data
    assert len(data["equipment"]) == 1
    assert "data" in data
    assert data["party"] == {"id": 1, "name": "Famille McTrickfoot"}
    assert data["player"] == {"id": 1, "name": "Balthazar"}


def test_update_characters(client):
    initial_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert initial_data["name"] == "Douglas McTrickfoot"
    assert initial_data["data"]["scores"]["strength"] == 8
    assert_status_and_return_data(
        client.put,
        "/api/character/douglas-mctrickfoot",
        status_code=200,
        json={"name": "Ronald McDonald", "data": {"scores": {"strength": 10}}},
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert updated_data["name"] == "Ronald McDonald"
    assert updated_data["data"]["scores"]["strength"] == 10


def test_update_with_invalid_payload(client):
    update_response = client.put(
        "/api/character/douglas-mctrickfoot",
        json={"name": "Ronald McDonald", "invalid": "field"},
    )
    assert update_response.status_code == 422
