"""
This module contains a Caribou migration.

Migration Name: character_party_not_null
Migration Version: 20230621103657
"""

from caribou import transaction


def upgrade(connection):
    statements = [
        "BEGIN TRANSACTION;",
        "ALTER TABLE character RENAME COLUMN party_id TO party_id_nullable;",
        "ALTER TABLE character ADD party_id INTEGER NOT NULL DEFAULT 0 REFERENCES party(id);",
        "UPDATE character SET party_id = party_id_nullable;",
        "ALTER TABLE character DROP COLUMN party_id_nullable;",
        "COMMIT;",
    ]
    with transaction(connection):
        for statement in statements:
            connection.execute(statement)


def downgrade(connection):
    statements = [
        "BEGIN TRANSACTION;",
        "ALTER TABLE character RENAME COLUMN party_id TO party_id_not_nullable;",
        "ALTER TABLE character ADD party_id INTEGER REFERENCES party(id);",
        "UPDATE character SET party_id = party_id_not_nullable;",
        "ALTER TABLE character DROP COLUMN party_id_not_nullable;",
        "COMMIT;",
    ]
    with transaction(connection):
        for statement in statements:
            connection.execute(statement)
