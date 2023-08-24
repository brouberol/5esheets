def test_sqlite_version(unauthed_client):
    assert unauthed_client.get("/api/debug/sqlite-version").json() == {
        "version": "3.42.0"
    }
