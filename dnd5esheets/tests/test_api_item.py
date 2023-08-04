from sqlalchemy import select

from dnd5esheets.models import Item

from .utils import assert_status_and_return_data


def test_get_item(client):
    data = assert_status_and_return_data(client.get, "/api/item/1", status_code=200)
    assert data["name"] == "Arrow"


def test_get_item_etag(client):
    response = client.get("/api/item/1")
    assert "etag" in response.headers
    etag = response.headers["etag"]

    response2 = client.get("/api/item/1")
    assert etag == response2.headers["etag"]


def test_item_schema(client, session):
    item_ids = session.execute(select(Item.id)).scalars().all()
    for item_id in item_ids:
        resp = client.get(f"/api/item/{item_id}")
        assert resp.status_code == 200, (item_id, resp.status_code)
