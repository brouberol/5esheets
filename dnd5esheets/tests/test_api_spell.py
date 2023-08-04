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
