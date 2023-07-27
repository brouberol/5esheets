import pytest
from sqlalchemy import exc as sa_exc

from dnd5esheets.models import Character, EquippedItem, Item, Spell


def test_update_in_model_json_field(session):
    character = session.get(Character, 1)
    assert character.name == "Douglas McTrickfoot"
    assert character.data["abilities"]["strength"] == {
        "score": 8,
        "proficiency": 0,
        "save": 0,
        "modifier": 0,
    }
    # We update a root field, as well as a nested field, and we make sure that
    # only these fields get overridden
    character.update_from_dict(
        {"name": "Mr DingDong", "data": {"abilities": {"strength": {"score": 10}}}}
    )
    assert character.name == "Mr DingDong"
    assert character.data["abilities"]["strength"] == {
        "score": 10,
        "proficiency": 0,
        "save": 0,
        "modifier": 0,
    }


def test_duplicate_character_slug(session):
    char1 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=1, party_id=1
    )
    session.add(char1)
    session.commit()

    # Same slug, different player, so that's ok
    char2 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=2, party_id=2
    )
    session.add(char2)
    session.commit()

    # Duplicate slug/player than with char1
    char3 = Character(
        name="Ronald McDonald", slug="ronald-mcdonald", player_id=1, party_id=1
    )
    session.add(char3)
    with pytest.raises(sa_exc.IntegrityError):
        session.commit()


def test_delete_character_cascade(session):
    douglas = session.get(Character, 1)
    equipped_item_ids = [equipped_item.id for equipped_item in douglas.equipment]
    equipment_item_ids = [equipped_item.item_id for equipped_item in douglas.equipment]
    session.delete(douglas)
    session.commit()

    # Make sure the items haven't been deleted when a character was deleted.
    # Safgeguard against me being clumsy with cascades
    for equipment_item_id in equipment_item_ids:
        assert session.get(Item, equipment_item_id) is not None
    for equipped_item_id in equipped_item_ids:
        assert session.get(EquippedItem, equipped_item_id) is None


def test_character_level_validation(session):
    Character(name="Ronald McDonald", player_id=1, party_id=1)  # level = None, OK
    Character(name="Ronald McDonald", player_id=1, party_id=1, level=2)

    with pytest.raises(ValueError):
        Character(name="Ronald McDonald", player_id=1, party_id=1, level=30)

        
def test_spell_level_validation(session):
    with pytest.raises(ValueError):
        Spell(name="Abracadabra", level=10, school="C", data={})

    with pytest.raises(ValueError):
        Spell(name="Abracadabra", level=-1, school="C", data={})

    Spell(name="Abracadabra", level=1, school="C", data={})
