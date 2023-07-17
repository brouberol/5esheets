from dnd5esheets.models import Character


def test_update_in_model_json_field(db):
    character = db.get(Character, 1)
    assert character.name == "Douglas McTrickfoot"
    assert character.data["scores"] == {
        "strength": 8,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 12,
        "charisma": 14,
    }
    # We update a root field, as well as a nested field, and we make sure that
    # only these fields get overridden
    character.update_from_dict(
        {"name": "Mr DingDong", "data": {"scores": {"strength": 10}}}
    )
    assert character.name == "Mr DingDong"
    assert character.data["scores"] == {
        "strength": 10,
        "dexterity": 14,
        "constitution": 12,
        "intelligence": 18,
        "wisdom": 12,
        "charisma": 14,
    }
