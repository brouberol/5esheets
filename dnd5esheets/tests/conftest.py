import os
import shutil
from urllib.parse import urlparse

import pytest_asyncio
from fastapi.testclient import TestClient
from pytest import fixture

from dnd5esheets.app import app
from dnd5esheets.cli import (
    _populate_base_items,
    _populate_db_with_dev_data,
    _populate_spells,
)
from dnd5esheets.config import get_settings
from dnd5esheets.db import create_session, engine
from dnd5esheets.models import BaseModel, Character, Player


@fixture(scope="session")
def settings():
    return get_settings()


@fixture(scope="session")
def unauthed_client():
    return TestClient(app)


@fixture(autouse=True)
def _remove_all_tables_and_restore_pre_test_backup(settings):
    yield  # let the test run

    # Restore the backup
    db_file = urlparse(settings.DB_URI).path
    shutil.copyfile(db_file + ".bak", db_file)


@fixture(scope="session")
def client():
    _client = TestClient(app)
    _client.post(
        "/api/login/token", data={"username": "br@test.com", "password": "azerty"}
    )
    return _client


@fixture(scope="session", autouse=True)
def init_db(settings):
    # Create all tables
    BaseModel.metadata.create_all(bind=engine)

    # Insert test data in the db
    _populate_base_items(silent=True)
    _populate_spells(silent=True)
    _populate_db_with_dev_data(silent=True)

    # Prepare a greenfield db dump to be restored after each test
    db_file = urlparse(settings.DB_URI).path
    shutil.copyfile(db_file, db_file + ".bak")

    # Let all tests run
    yield

    # Cleanup after all the tests have run
    os.remove(db_file)
    os.remove(db_file + ".bak")


@fixture(scope="function")
def session():
    """A fixture automatically used for each test, providing a DB session.

    This makes sure that any side effect in database is reverted at the end of the test.

    """
    with create_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with create_session() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def douglas(async_session):
    return await async_session.get(Character, 1)


@pytest_asyncio.fixture(scope="function")
async def balthazar(async_session):
    return await async_session.get(Player, 1)
