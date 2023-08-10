from sqlalchemy import select

from dnd5esheets.models import Spell

from .utils import assert_status_and_return_data


def test_get_spell(client):
    data = assert_status_and_return_data(client.get, "/api/spell/1", status_code=200)

    assert data["name"] == "Blade of Disaster"


def test_get_spell_etag(client):
    response = client.get("/api/spell/1")
    assert "etag" in response.headers
    etag = response.headers["etag"]

    response2 = client.get("/api/spell/1")
    assert etag == response2.headers["etag"]


def test_spell_schema(client, session):
    spell_ids = session.execute(select(Spell.id)).scalars().all()
    for spell_id in spell_ids:
        resp = client.get(f"/api/spell/{spell_id}")
        assert resp.status_code == 200, (spell_id, resp.status_code)


def test_search_spell(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/spell/search",
        params={"search_term": "name:magic missile"},
        status_code=200,
    )
    assert len(search_results) == 1
    assert sorted(search_results[0].keys()) == [
        "language",
        "name",
        "rank",
        "resource_id",
    ]
    assert search_results[0]["language"] == "en"
    assert search_results[0]["name"] == "Magic Missile"
    assert search_results[0]["resource_id"] == 330


def test_search_spell_with_limit(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/spell/search",
        params={"search_term": "fire"},
        status_code=200,
    )
    assert len(search_results) == 10

    search_results = assert_status_and_return_data(
        client.get,
        "/api/spell/search",
        params={"search_term": "fire", "limit": 5},
        status_code=200,
    )
    assert len(search_results) == 5


def test_search_spell_with_favored_language(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/spell/search",
        params={"search_term": "name:aid"},
        status_code=200,
    )
    assert search_results[0]["language"] == "en"

    search_results = assert_status_and_return_data(
        client.get,
        "/api/spell/search",
        params={"search_term": "name:aid", "favored_language": "fr"},
        status_code=200,
    )
    assert search_results[0]["language"] == "fr"
