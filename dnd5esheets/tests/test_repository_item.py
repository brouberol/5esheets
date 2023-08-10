from copy import deepcopy

import pytest

from dnd5esheets.cli import _populate_base_items
from dnd5esheets.models import Item
from dnd5esheets.repositories.item import ItemRepository


@pytest.mark.asyncio
async def test_get_item_by_id(async_session):
    spell = await ItemRepository.get_by_id(async_session, id=1)
    assert spell.name == "Arrow"


@pytest.mark.asyncio
async def test_search_item(async_session):
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 2
    result_resource_ids = sorted([result.resource_id for result in search_results])
    assert result_resource_ids == [1, 2]


@pytest.mark.asyncio
async def test_trigger_item_after_delete_and_insert(async_session):
    arrow = await async_session.get(Item, 1)
    await async_session.delete(arrow)
    await async_session.commit()
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 1
    result_resource_ids = sorted([result.resource_id for result in search_results])
    assert result_resource_ids == [2]

    _populate_base_items(silent=True)  # reinsert all items
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 2
    result_resource_ids = sorted([result.resource_id for result in search_results])
    assert result_resource_ids == [1, 2]


@pytest.mark.asyncio
async def test_trigger_iter_after_update(async_session):
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    arrow_search_result = [res for res in search_results if res.resource_id == 1][0]
    assert arrow_search_result.description is None

    # Add a description to the item
    arrow = await async_session.get(Item, 1)
    data = deepcopy(arrow.data)
    data["meta"]["description"] = "A very useful set of arrows"
    arrow.data = data
    async_session.add(arrow)
    await async_session.commit()

    # Make sure the new description was propagated to the search index
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    arrow_search_result = [res for res in search_results if res.resource_id == 1][0]
    assert arrow_search_result.description == "A very useful set of arrows"


@pytest.mark.asyncio
async def test_search_item_with_favored_language(async_session):
    search_results = await ItemRepository.search(async_session, search_term="chain")
    assert search_results[0].language == "en"

    search_results_favoring_fr = await ItemRepository.search(
        async_session, search_term="arm", favored_language="fr"
    )
    assert search_results_favoring_fr[0].language == "fr"


@pytest.mark.asyncio
async def test_search_item_with_limit(async_session):
    search_results = await ItemRepository.search(async_session, search_term="arrow")
    assert len(search_results) == 2
    search_results = await ItemRepository.search(
        async_session, search_term="arm", limit=1
    )
    assert len(search_results) == 1


@pytest.mark.asyncio
async def test_search_item_via_specific_field(async_session):
    search_results = await ItemRepository.search(
        async_session, search_term="name:fleche"
    )
    assert len(search_results) == 1
    assert search_results[0].name == "Flèche"

    search_results = await ItemRepository.search(async_session, search_term="fleche")
    assert len(search_results) == 2
    assert sorted([r.name for r in search_results]) == [
        "Arc long",
        "Flèche",
    ]
