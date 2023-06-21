"""
This module contains a Caribou migration.

Migration Name: character_player_not_null
Migration Version: 20230621100955
"""

from caribou import transaction


def upgrade(connection):
    statements = [
        "BEGIN TRANSACTION;",
        "ALTER TABLE character RENAME COLUMN player_id TO player_id_nullable;",
        "ALTER TABLE character ADD player_id INTEGER NOT NULL DEFAULT 0 REFERENCES player(id);",
        "UPDATE character SET player_id = player_id_nullable;",
        "ALTER TABLE character DROP COLUMN player_id_nullable;",
        "COMMIT;",
    ]
    with transaction(connection):
        for statement in statements:
            connection.execute(statement)


def downgrade(connection):
    statements = [
        "BEGIN TRANSACTION;",
        "ALTER TABLE character RENAME COLUMN player_id TO player_id_not_nullable;",
        "ALTER TABLE character ADD player_id INTEGER REFERENCES player(id);",
        "UPDATE character SET player_id = player_id_not_nullable;",
        "ALTER TABLE character DROP COLUMN player_id_not_nullable;",
        "COMMIT;",
    ]
    with transaction(connection):
        for statement in statements:
            connection.execute(statement)
