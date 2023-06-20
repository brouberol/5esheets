"""
This module contains a Caribou migration.

Migration Name: first_migration
Migration Version: 20230614145526
"""


def upgrade(connection):
    statements = [
        """CREATE TABLE IF NOT EXISTS character(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        slug VARCHAR(255),
        class VARCHAR(80),
        level INTEGER,
        json_data TEXT NOT NULL DEFAULT '{}'
        )
        """,
        "CREATE INDEX IF NOT EXISTS character_slug ON character(slug);",
    ]
    for statement in statements:
        connection.execute(statement)


def downgrade(connection):
    connection.execute("DROP TABLE sheets;")
