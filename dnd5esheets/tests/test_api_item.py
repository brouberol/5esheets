from .utils import assert_status_and_return_data


def test_list_characters(client):
    data = assert_status_and_return_data(client.get, "/api/item/1", status_code=200)

    assert data["name"] == "Arrow"
