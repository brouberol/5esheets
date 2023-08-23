import pytest

from dnd5esheets.exceptions import DuplicateModel, ModelNotFound
from dnd5esheets.repositories.character import CharacterRepository
from dnd5esheets.schemas import CreateCharacterSchema, UpdateCharacterSchema


@pytest.mark.asyncio
async def test_list_all_no_owner(async_session):
    assert len(await CharacterRepository.list_all(async_session)) == 6


@pytest.mark.asyncio
async def test_list_all_with_owner(async_session):
    assert len(await CharacterRepository.list_all(async_session, owner_id=1)) == 1


@pytest.mark.asyncio
async def test_get_character_by_slug_with_owner(async_session, douglas):
    assert (
        await CharacterRepository.get_by_slug(
            async_session, slug="douglas-mctrickfoot", owner_id=1
        )
        == douglas
    )


@pytest.mark.asyncio
async def test_get_unknown_character(async_session):
    with pytest.raises(ModelNotFound):
        await CharacterRepository.get_by_slug(
            async_session, slug="ronald-mcdonald", owner_id=1
        )


@pytest.mark.asyncio
async def test_update_character(async_session):
    douglas_before_update = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert douglas_before_update.level == 4
    assert douglas_before_update.data["abilities"]["dexterity"]["score"] == 14
    await CharacterRepository.update(
        async_session,
        slug="douglas-mctrickfoot",
        body=UpdateCharacterSchema(
            level=5, data={"abilities": {"dexterity": {"score": 15}}}
        ),
    )
    douglas_after_update = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert douglas_after_update.level == 5
    assert douglas_before_update.data["abilities"]["dexterity"]["score"] == 15


@pytest.mark.asyncio
async def test_create_character(async_session):
    ronald = await CharacterRepository.create(
        async_session,
        character_data=CreateCharacterSchema(name="Ronald McDonald", party_id=1),
        owner_id=1,
    )
    assert ronald.name == "Ronald McDonald"
    assert ronald.slug == "ronald-mcdonald"
    assert ronald.level is None
    assert ronald.class_ is None
    assert ronald.data is None
    assert ronald.player_id == 1
    assert ronald.party_id == 1


@pytest.mark.asyncio
async def test_create_character_in_party_player_isnt_a_member_of(async_session):
    with pytest.raises(ModelNotFound):
        await CharacterRepository.create(
            async_session,
            character_data=CreateCharacterSchema(name="Ronald McDonald", party_id=2),
            owner_id=1,
        )


@pytest.mark.asyncio
async def test_create_duplicate_character(async_session):
    with pytest.raises(DuplicateModel):
        await CharacterRepository.create(
            async_session,
            character_data=CreateCharacterSchema(
                name="Douglas McTrickfoot", party_id=1
            ),
            owner_id=1,
        )


@pytest.mark.asyncio
async def test_character_etag_stability(async_session):
    etag = await CharacterRepository.etag(
        async_session, slug="douglas-mctrickfoot", owner_id=1
    )
    # Nothing has changed, the etag is the same
    assert (
        await CharacterRepository.etag(
            async_session, slug="douglas-mctrickfoot", owner_id=1
        )
        == etag
    )
    await CharacterRepository.update(
        async_session,
        slug="douglas-mctrickfoot",
        body=UpdateCharacterSchema(level=5),
    )
    # Something related to the character has changed, thus the etag changed as well
    assert (
        await CharacterRepository.etag(
            async_session, slug="douglas-mctrickfoot", owner_id=1
        )
        != etag
    )


@pytest.mark.asyncio
async def test_delete_character(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert douglas is not None
    await CharacterRepository.delete(async_session, slug="douglas-mctrickfoot")
    with pytest.raises(ModelNotFound):
        await CharacterRepository.get_by_slug(async_session, slug="douglas-mctrickfoot")


@pytest.mark.asyncio
async def test_change_equipment_item_equipped_status(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert douglas.equipment[0].equipped is False

    douglas = await CharacterRepository.change_equipment_item_equipped_status(
        async_session,
        slug="douglas-mctrickfoot",
        equipped_item_id=douglas.equipment[0].id,
        equipped=True,
    )
    assert douglas.equipment[0].equipped is True

    douglas = await CharacterRepository.change_equipment_item_equipped_status(
        async_session,
        slug="douglas-mctrickfoot",
        equipped_item_id=douglas.equipment[0].id,
        equipped=False,
    )
    assert douglas.equipment[0].equipped is False


@pytest.mark.asyncio
async def test_change_known_spell_prepared_status(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert douglas.spellbook[0].prepared is True

    douglas = await CharacterRepository.change_known_spell_prepared_status(
        async_session,
        slug="douglas-mctrickfoot",
        known_spell_id=douglas.spellbook[0].id,
        prepared=False,
    )
    assert douglas.spellbook[0].prepared is False

    douglas = await CharacterRepository.change_known_spell_prepared_status(
        async_session,
        slug="douglas-mctrickfoot",
        known_spell_id=douglas.spellbook[0].id,
        prepared=True,
    )
    assert douglas.spellbook[0].prepared is True


@pytest.mark.asyncio
async def test_learn_spell(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.spellbook) == 7
    await CharacterRepository.learn_spell(
        async_session,
        slug="douglas-mctrickfoot",
        spell_id=45,
        prepared=True,
    )
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.spellbook) == 8
    assert douglas.spellbook[-1].spell.id == 45
    assert douglas.spellbook[-1].prepared is True


@pytest.mark.asyncio
async def test_forget_spell(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.spellbook) == 7
    known_spell_id = douglas.spellbook[-1].id
    await CharacterRepository.forget_spell(
        async_session,
        slug="douglas-mctrickfoot",
        known_spell_id=known_spell_id,
    )
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.spellbook) == 6


@pytest.mark.asyncio
async def test_add_item_to_equipment(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.equipment) == 1
    await CharacterRepository.add_item_to_equipment(
        async_session,
        slug="douglas-mctrickfoot",
        item_id=30,
    )
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.equipment) == 2
    assert douglas.equipment[-1].item.id == 30


@pytest.mark.asyncio
async def test_from_item_from_equipment(async_session):
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.equipment) == 1
    equipped_item_id = douglas.equipment[-1].id
    await CharacterRepository.remove_item_from_equipment(
        async_session,
        slug="douglas-mctrickfoot",
        equipped_item_id=equipped_item_id,
    )
    douglas = await CharacterRepository.get_by_slug(
        async_session, slug="douglas-mctrickfoot"
    )
    assert len(douglas.equipment) == 0
