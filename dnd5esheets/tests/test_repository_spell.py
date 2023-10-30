from copy import deepcopy

import pytest

from dnd5esheets.cli import _populate_spells
from dnd5esheets.models import Spell
from dnd5esheets.repositories.spell import SpellRepository


@pytest.mark.asyncio
async def test_get_spell_by_id(async_session):
    spell = await SpellRepository.get_by_id(async_session, id=1)
    assert spell.name == "Blade of Disaster"


@pytest.mark.asyncio
async def test_search_spell(async_session):
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 6
    result_resource_ids = sorted([result.name for result in search_results])
    assert result_resource_ids == [
        "Antimagic Field",
        "Cordon of Arrows",
        "Flame Arrows",
        "Lightning Arrow",
        "Melf's Acid Arrow",
        "Wind Wall",
    ]


@pytest.mark.asyncio
async def test_trigger_spell_after_delete_and_insert(async_session):
    arrow = await async_session.get(Spell, 51)
    await async_session.delete(arrow)
    await async_session.commit()
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 5
    result_resource_ids = sorted([result.resource_id for result in search_results])
    assert 51 not in result_resource_ids

    _populate_spells(silent=True)  # reinsert all spells
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 6
    result_resource_ids = sorted([result.resource_id for result in search_results])
    assert 51 in result_resource_ids


@pytest.mark.asyncio
async def test_trigger_iter_after_update(async_session):
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    arrow_search_result = [res for res in search_results if res.resource_id == 51][0]

    # Add a description to the spell
    arrow = await async_session.get(Spell, 51)
    data = deepcopy(arrow.data)
    data["meta"]["description"] = "A powerful arrow spell"
    arrow.data = data
    async_session.add(arrow)
    await async_session.commit()

    # Make sure the new description was propagated to the search index
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    arrow_search_result = [res for res in search_results if res.resource_id == 51][0]
    assert arrow_search_result.description == "A powerful arrow spell"


@pytest.mark.asyncio
async def test_search_spell_with_favored_language(async_session):
    search_results = await SpellRepository.search(async_session, search_term="aid")
    assert search_results[0].language == "fr"

    search_results_favoring_en = await SpellRepository.search(
        async_session, search_term="aid", favored_language="en"
    )
    assert search_results_favoring_en[0].language == "en"


@pytest.mark.asyncio
async def test_search_spell_with_limit(async_session):
    search_results = await SpellRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 6
    search_results = await SpellRepository.search(async_session, search_term="arrow", limit=5)
    assert len(search_results) == 5


@pytest.mark.asyncio
async def test_search_spell_via_specific_field(async_session):
    search_results = await SpellRepository.search(async_session, search_term="name:fleche")
    assert len(search_results) == 3
    assert sorted([r.name for r in search_results]) == [
        "Cordon de flèches",
        "Flèche de foudre",
        "Flèches enflammées",
    ]

    search_results = await SpellRepository.search(async_session, search_term="fleche")
    assert len(search_results) == 5
    assert sorted([r.name for r in search_results]) == [
        "Champ antimagie",
        "Cordon de flèches",
        "Flèche de foudre",
        "Flèches enflammées",
        "Mur de vent",
    ]
