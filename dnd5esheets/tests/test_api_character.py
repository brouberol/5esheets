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
    assert initial_data["data"]["abilities"]["strength"]["score"] == 8
    assert_status_and_return_data(
        client.put,
        "/api/character/douglas-mctrickfoot",
        status_code=200,
        json={
            "name": "Ronald McDonald",
            "data": {"abilities": {"strength": {"score": 10}}},
        },
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert updated_data["name"] == "Ronald McDonald"
    assert updated_data["data"]["abilities"]["strength"]["score"] == 10


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


def test_describe_character_with_etag(client):
    response = client.get("/api/character/douglas-mctrickfoot")
    assert response.status_code == 200
    assert "ETag" in response.headers

    new_response = client.get(
        "/api/character/douglas-mctrickfoot",
        headers={"If-None-Match": response.headers["ETag"]},
    )
    assert new_response.status_code == 304  # The Etag is the same

    update_response = client.put(
        "/api/character/douglas-mctrickfoot",
        json={"level": "5"},  # direct update to the Character
    )
    assert update_response.status_code == 200

    response_after_update = client.get(
        "/api/character/douglas-mctrickfoot",
        headers={"If-None-Match": response.headers["ETag"]},
    )
    assert response_after_update.status_code == 200  # the etag has changed

    update_response = client.put(
        "/api/party/1",
        json={
            "name": "Los Pollos Hermanos"
        },  # indirect update to the Character, as this is a related field
    )
    assert update_response.status_code == 200

    new_response_after_party_update = client.get(
        "/api/character/douglas-mctrickfoot",
        headers={"If-None-Match": response_after_update.headers["ETag"]},
    )
    assert (
        new_response_after_party_update.status_code == 200
    )  # the etag has changed again


def test_delete_character(client):
    assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    delete_response = client.delete("/api/character/douglas-mctrickfoot")
    assert delete_response.status_code == 204
    assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=404
    )


def test_delete_character_from_non_owner(client):
    assert_status_and_return_data(
        client.get, "/api/character/trevor-mctrickfoot", status_code=404
    )


def test_change_character_equipment_item_equipped_status(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data["equipment"][0]["equipped"] is False
    equipment_item_id = data["equipment"][0]["id"]
    assert_status_and_return_data(
        client.put,
        f"/api/character/douglas-mctrickfoot/equipment/{equipment_item_id}/equip",
        status_code=200,
    )
    data_after_update = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data_after_update["equipment"][0]["equipped"] is True
    assert_status_and_return_data(
        client.put,
        f"/api/character/douglas-mctrickfoot/equipment/{equipment_item_id}/unequip",
        status_code=200,
    )
    data_after_update = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data_after_update["equipment"][0]["equipped"] is False


def test_change_known_spell_prepared_status(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data["spellbook"][0]["prepared"] is True
    known_spell_id = data["spellbook"][0]["id"]
    assert_status_and_return_data(
        client.put,
        f"/api/character/douglas-mctrickfoot/spellbook/{known_spell_id}/unprepare",
        status_code=200,
    )
    data_after_update = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data_after_update["spellbook"][0]["prepared"] is False
    assert_status_and_return_data(
        client.put,
        f"/api/character/douglas-mctrickfoot/spellbook/{known_spell_id}/prepare",
        status_code=200,
    )
    data_after_update = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert data_after_update["spellbook"][0]["prepared"] is True


def test_learn_spell(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(data["spellbook"]) == 7
    assert_status_and_return_data(
        client.put, "/api/character/douglas-mctrickfoot/spellbook/30", status_code=200
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(updated_data["spellbook"]) == 8
    assert updated_data["spellbook"][-1]["spell"]["name"] == "Ceremony"


def test_forget_spell(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(data["spellbook"]) == 7
    known_spell_id = data["spellbook"][0]["id"]
    assert_status_and_return_data(
        client.delete,
        f"/api/character/douglas-mctrickfoot/spellbook/{known_spell_id}",
        status_code=200,
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(updated_data["spellbook"]) == 6
    assert updated_data["spellbook"][-1]["id"] != known_spell_id


def test_add_item_to_equipment(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(data["equipment"]) == 1
    assert_status_and_return_data(
        client.put, "/api/character/douglas-mctrickfoot/equipment/10", status_code=200
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(updated_data["equipment"]) == 2
    assert updated_data["equipment"][-1]["item"]["name"] == "Club"


def test_remove_item_from_equipment(client):
    data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(data["equipment"]) == 1
    equipped_item_id = data["equipment"][0]["id"]
    assert_status_and_return_data(
        client.delete,
        f"/api/character/douglas-mctrickfoot/equipment/{equipped_item_id}",
        status_code=200,
    )
    updated_data = assert_status_and_return_data(
        client.get, "/api/character/douglas-mctrickfoot", status_code=200
    )
    assert len(updated_data["equipment"]) == 0
