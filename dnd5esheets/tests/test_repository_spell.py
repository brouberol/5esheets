import pytest

from dnd5esheets.repositories.spell import SpellRepository


@pytest.mark.asyncio
async def test_get_spell_by_id(async_session):
    spell = await SpellRepository.get_by_id(async_session, id=1)
    assert spell.name == "Blade of Disaster"
