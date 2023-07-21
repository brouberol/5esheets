import pytest
from sqlalchemy import exc as sa_exc

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


def test_duplicate_character_slug(db):
    char1 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=1, party_id=1
    )
    db.add(char1)
    db.commit()

    # Same slug, different player, so that's ok
    char2 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=2, party_id=2
    )
    db.add(char2)
    db.commit()

    # Duplicate slug/player than with char1
    char3 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=1, party_id=1
    )
    db.add(char3)
    with pytest.raises(sa_exc.IntegrityError):
        db.commit()
