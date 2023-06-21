"""
This module contains a Caribou migration.

Migration Name: add_player_model
Migration Version: 20230621092853
"""


def upgrade(connection):
    statements = [
        """CREATE TABLE IF NOT EXISTS player(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255)
        );""",
        # We'll need to specify that player_id can't be null in another migration
        "ALTER TABLE character ADD player_id INTEGER REFERENCES player(id);",
    ]
    for statement in statements:
        connection.execute(statement)


def downgrade(connection):
    statements = ["ALTER TABLE character DROP COLUMN player_id;", "DROP TABLE player;"]
    for statement in statements:
        connection.execute(statement)
