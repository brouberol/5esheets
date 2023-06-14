"""
This module contains a Caribou migration.

Migration Name: first_migration
Migration Version: 20230614145526
"""


def upgrade(connection):
    statements = [
        """CREATE TABLE IF NOT EXISTS sheets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_name VARCHAR(255),
        character_slug VARCHAR(255),
        character_class VARCHAR(50),
        character_level INTEGER,
        character_json_data TEXT NOT NULL
    );
    """,
        """
    CREATE INDEX IF NOT EXISTS sheets_character_slug ON sheets(character_slug);
    """,
    ]
    for statement in statements:
        connection.execute(statement)


def downgrade(connection):
    connection.execute("DROP TABLE sheets;")
