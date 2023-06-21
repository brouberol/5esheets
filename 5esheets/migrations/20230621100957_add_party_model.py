"""
This module contains a Caribou migration.

Migration Name: add_party_model
Migration Version: 20230621100750
"""


def upgrade(connection):
    statements = [
        """CREATE TABLE IF NOT EXISTS party (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255)
        );""",
        "ALTER TABLE character ADD COLUMN party_id INTEGER REFERENCES party(id);",
    ]
    for statement in statements:
        connection.execute(statement)


def downgrade(connection):
    statements = ["ALTER TABLE character DROP COLUMN party_id;", "DROP TABLE party;"]
    for statement in statements:
        connection.execute(statement)
