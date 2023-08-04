import pytest

from dnd5esheets.exceptions import ModelNotFound
from dnd5esheets.repositories.party import PartyRepository
from dnd5esheets.schemas import UpdatePartySchema


@pytest.mark.asyncio
async def test_list_all_no_owner(async_session):
    assert len(await PartyRepository.list_all(async_session)) == 2


@pytest.mark.asyncio
async def test_list_all_with_owner(async_session):
    assert len(await PartyRepository.list_all(async_session, owner_id=1)) == 1


@pytest.mark.asyncio
async def test_get_by_id_if_member_of_with_righful_owner(async_session):
    party = await PartyRepository.get_by_id_if_member_of(
        async_session, id=1, member_id=1
    )
    assert len(party.members) == 4


@pytest.mark.asyncio
async def test_get_by_id_if_member_of_with_unrighful_owner(async_session):
    with pytest.raises(ModelNotFound):
        await PartyRepository.get_by_id_if_member_of(async_session, id=2, member_id=1)


@pytest.mark.asyncio
async def test_update_if_member_of_with_righful_owner(async_session):
    party = await PartyRepository.update_if_member_of(
        async_session,
        id=1,
        member_id=1,
        body=UpdatePartySchema(name="La Famille Adams"),
    )
    assert party.name == "La Famille Adams"


@pytest.mark.asyncio
async def test_update_if_member_of_with_unrighful_owner(async_session):
    with pytest.raises(ModelNotFound):
        await PartyRepository.update_if_member_of(
            async_session,
            id=2,
            member_id=1,
            body=UpdatePartySchema(name="La Famille Adams"),
        )
