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


def test_create_new_character(client):
    created_data = assert_status_and_return_data(
        client.post,
        "/api/character/new",
        json={"name": "Ronald McDonald", "party_id": 1},
        status_code=200,
    )
    assert created_data["name"] == "Ronald McDonald"
    assert created_data["slug"] == "ronald-mcdonald"
    assert created_data["player"]["name"] == "Balthazar"
    assert created_data["party"]["name"] == "Famille McTrickfoot"
    assert created_data["class_"] is None
    assert created_data["data"] is None
    assert created_data["level"] is None

    # Make sure the character is now saved to DB
    display_data = assert_status_and_return_data(
        client.get, f"/api/character/{created_data['slug']}", status_code=200
    )
    assert created_data == display_data


def test_create_new_character_in_party_with_no_player_character(client):
    assert_status_and_return_data(
        client.post,
        "/api/character/new",
        json={"name": "Ronald McDonald", "party_id": 2},
        status_code=404,
    )


def test_create_duplicate_character_for_same_player(client):
    assert_status_and_return_data(
        client.post,
        "/api/character/new",
        json={"name": "Ronald McDonald", "party_id": 1},
        status_code=200,
    )
    assert_status_and_return_data(
        client.post,
        "/api/character/new",
        json={"name": "Ronald McDonald", "party_id": 1},
        status_code=400,
    )

