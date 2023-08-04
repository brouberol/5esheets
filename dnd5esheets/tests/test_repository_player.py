import pytest

from dnd5esheets.exceptions import ModelNotFound
from dnd5esheets.repositories.player import PlayerRepository
from dnd5esheets.schemas import UpdatePlayerSchema


@pytest.mark.asyncio
async def test_get_player_by_id(async_session, balthazar):
    assert await PlayerRepository.get_by_id(async_session, id=1) == balthazar


@pytest.mark.asyncio
async def test_get_player_by_id_not_found(async_session):
    with pytest.raises(ModelNotFound):
        await PlayerRepository.get_by_id(async_session, id=10)


@pytest.mark.asyncio
async def test_get_player_by_email(async_session, balthazar):
    assert (
        await PlayerRepository.get_by_email(async_session, email="br@test.com")
        == balthazar
    )


@pytest.mark.asyncio
async def test_get_player_by_email_not_found(async_session):
    with pytest.raises(ModelNotFound):
        await PlayerRepository.get_by_email(async_session, email="nope@nope.nope")


@pytest.mark.asyncio
async def test_update_player(async_session):
    await PlayerRepository.update(
        async_session, id=1, body=UpdatePlayerSchema(name="brou")
    )
    assert (await PlayerRepository.get_by_id(async_session, id=1)).name == "brou"


@pytest.mark.asyncio
async def test_player_has_character_in_party(async_session):
    assert (
        await PlayerRepository.player_has_character_in_party(
            async_session, player_id=1, party_id=1
        )
        is True
    )


@pytest.mark.asyncio
async def test_player_has_no_character_in_party(async_session):
    assert (
        await PlayerRepository.player_has_character_in_party(
            async_session, player_id=1, party_id=2
        )
        is False
    )
