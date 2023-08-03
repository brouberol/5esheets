import pytest

from dnd5esheets.repositories.item import ItemRepository


@pytest.mark.asyncio
async def test_get_item_by_id(async_session):
    spell = await ItemRepository.get_by_id(async_session, id=1)
    assert spell.name == "Arrow"
