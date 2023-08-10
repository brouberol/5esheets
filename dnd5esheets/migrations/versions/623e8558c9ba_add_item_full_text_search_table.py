"""add_item_full_text_search_table

Revision ID: 623e8558c9ba
Revises: a4d56d02c64b
Create Date: 2023-08-09 15:45:46.542535

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "623e8558c9ba"
down_revision = "a4d56d02c64b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    ddls = [
        # Create a full text search index for items
        """
        CREATE VIRTUAL TABLE item_search_index USING fts5(
            item_id UNINDEXED,
            language UNINDEXED,
            name,
            description,
            tokenize=porter
        )
        """,
        # Every time a new item is created, insert a new row into the item_search_index FTS table,
        # one for the default english name/description, and one per translated name/description
        """
        CREATE TRIGGER item_after_insert
            AFTER INSERT ON item
        BEGIN
            INSERT INTO item_search_index (rowid, item_id, language, name, description) VALUES (
                cast(hex('en') as integer) + new.id,
                new.id,
                'en',
                new.name,
                json_extract(new.json_data, '$.meta.description')
            );
            INSERT INTO item_search_index (rowid, item_id, language, name, description)
                SELECT
                    cast(hex(json_each.key) as integer) + new.id,
                    new.id,
                    json_each.key,
                    json_extract(json_each.value, '$.name'),
                    json_extract(json_each.value, '$.description')
                FROM json_each(json_extract(new.json_data, '$.meta.translations'));
        END;
        """,
        # Populate the search index with the existing items
        """
        INSERT INTO item_search_index (rowid, item_id, language, name, description)
            SELECT
                cast(hex('en') as integer) + id,
                id,
                'en',
                name,
                json_extract(json_data, '$.meta.description')
            FROM item;
        """,
        """
        INSERT INTO item_search_index (rowid, item_id, language, name, description)
            SELECT
                cast(hex(json_each.key) as integer) + item.id,
                item.id,
                json_each.key,
                json_extract(json_each.value, '$.name'),
                json_extract(json_each.value, '$.description')
            FROM item, json_each(json_extract(item.json_data, '$.meta.translations'));
        """,
        # Every time an item is deleted from DB, delete it from the search index
        """
        CREATE TRIGGER item_after_delete
            AFTER DELETE ON item
        BEGIN
            DELETE FROM item_search_index WHERE item_id=old.id;
        END;
        """,
        # Every time an item is update in DB, update it in the search index as well
        """
        CREATE TRIGGER item_after_update
            AFTER UPDATE ON item
            WHEN old.name <> new.name
                OR old.json_data <> new.json_data
        BEGIN
            REPLACE INTO item_search_index (rowid, item_id, language, name, description) VALUES (
                cast(hex('en') as integer) + new.id,
                new.id,
                'en',
                new.name,
                json_extract(new.json_data, '$.meta.description')
            );
            REPLACE INTO item_search_index (rowid, item_id, language, name, description)
                SELECT
                    cast(hex(json_each.key) as integer) + new.id,
                    new.id,
                    json_each.key,
                    json_extract(json_each.value, '$.name'),
                    json_extract(json_each.value, '$.description')
                FROM json_each(json_extract(new.json_data, '$.meta.translations'));
        END
        """,
    ]
    for stmt in ddls:
        op.execute(stmt)


def downgrade() -> None:
    ddls = [
        "DROP TRIGGER item_after_update",
        "DROP TRIGGER item_after_delete",
        "DROP TRIGGER item_after_insert",
        "DROP TABLE item_search_index",
    ]
    for stmt in ddls:
        op.execute(stmt)
