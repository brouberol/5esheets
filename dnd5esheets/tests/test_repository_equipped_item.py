import pytest

from dnd5esheets.repositories.equipped_item import EquippedItemRepository


@pytest.mark.asyncio
async def test_change_equipped_item_equipped_status(async_session):
    equipped_item = await EquippedItemRepository.change_equipped_status(
        async_session, id=1, equipped=False
    )
    assert equipped_item.equipped is False

    equipped_item = await EquippedItemRepository.change_equipped_status(
        async_session, id=1, equipped=True
    )
    assert equipped_item.equipped is True
