import pytest

from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.schemas import UpdatePartySchema


@pytest.mark.asyncio
async def test_list_all_no_owner(async_session):
    assert len(await PartyRepository.list_all(async_session)) == 2


@pytest.mark.asyncio
async def test_list_all_with_owner(async_session):
    assert len(await PartyRepository.list_all(async_session, owner_id=1)) == 1


@pytest.mark.asyncio
async def test_update(async_session):
    party = await PartyRepository.update(
        async_session,
        id=1,
        body=UpdatePartySchema(name="La Famille Adams"),
    )
    assert party.name == "La Famille Adams"
