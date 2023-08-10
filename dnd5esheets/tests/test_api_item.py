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


def test_search_item(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/item/search",
        params={"search_term": "name:fleche"},
        status_code=200,
    )
    assert len(search_results) == 1
    assert sorted(search_results[0].keys()) == [
        "language",
        "name",
        "rank",
        "resource_id",
    ]
    assert search_results[0]["language"] == "fr"
    assert search_results[0]["name"] == "Flèche"
    assert search_results[0]["resource_id"] == 1


def test_search_item_with_limit(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/item/search",
        params={"search_term": "arm"},
        status_code=200,
    )
    assert len(search_results) == 10

    search_results = assert_status_and_return_data(
        client.get,
        "/api/item/search",
        params={"search_term": "arm", "limit": 5},
        status_code=200,
    )
    assert len(search_results) == 5


def test_search_item_with_favored_language(client):
    search_results = assert_status_and_return_data(
        client.get,
        "/api/item/search",
        params={"search_term": "mail"},
        status_code=200,
    )
    assert search_results[0]["language"] == "en"

    search_results = assert_status_and_return_data(
        client.get,
        "/api/item/search",
        params={"search_term": "mail", "favored_language": "fr"},
        status_code=200,
    )
    assert search_results[0]["language"] == "fr"
