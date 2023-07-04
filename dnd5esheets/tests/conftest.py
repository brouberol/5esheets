import os
import subprocess
from urllib.parse import urlparse

from fastapi.testclient import TestClient
from pytest import fixture

from dnd5esheets.app import app
from dnd5esheets.cli import _populate_base_items, _populate_db_with_dev_data
from dnd5esheets.config import get_settings
from dnd5esheets.db import create_session, engine
from dnd5esheets.models import BaseModel


@fixture(scope="session")
def settings():
    return get_settings()


@fixture(scope="session")
def unauthed_client():
    return TestClient(app)


@fixture(scope="session")
def client():
    _client = TestClient(app)
    _client.post(
        "/api/login/token", data={"username": "br@test.com", "password": "azerty"}
    )
    _client.headers["X-CSRF-TOKEN"] = _client.cookies["csrf_access_token"]
    return _client


@fixture(scope="session", autouse=True)
def init_db(settings):
    # Create all tables
    BaseModel.metadata.create_all(bind=engine)

    # Insert test data in the db
    _populate_base_items(silent=True)
    _populate_db_with_dev_data(silent=True)

    # Prepare a greenfield db dump to be restored after each test
    db_file = urlparse(settings.DB_URI).path
    cmd = ["sqlite3", db_file, ".dump"]
    with open(db_file + ".bak", "w") as db_backup_file_fd:
        subprocess.run(cmd, stdout=db_backup_file_fd)

    # Let all tests run
    yield

    # Cleanup after all the tests have run
    os.remove(db_file)
    os.remove(db_file + ".bak")


@fixture(scope="function")
def db(settings):
    with create_session() as session:
        yield session

    # Ater the test has run, remove all tables
    BaseModel.metadata.drop_all(bind=engine)

    # Restore the backup
    db_file = urlparse(settings.DB_URI).path
    with open(db_file + ".bak") as db_backup_file_fd:
        subprocess.run(["sqlite3", db_file], stdin=db_backup_file_fd)
