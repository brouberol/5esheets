def test_sqlite_version(unauthed_client):
    sqlite_debug_info = unauthed_client.get("/api/debug/sqlite").json()
    assert sqlite_debug_info["version"] == "3.42.0"
    assert "ENABLE_FTS5" in sqlite_debug_info["compile_options"]
