"""add_spell_full_text_search_table

Revision ID: e3f5418ab972
Revises: 623e8558c9ba
Create Date: 2023-08-10 14:15:17.677897

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "e3f5418ab972"
down_revision = "623e8558c9ba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    ddls = [
        # Create a full text search index for spells
        """
        CREATE VIRTUAL TABLE spell_search_index USING fts5(
            spell_id UNINDEXED,
            language UNINDEXED,
            name,
            description,
            tokenize=porter
        )
        """,
        # Every time a new spell is created, insert a new row into the spell_search_index FTS table,
        # one for the default english name/description, and one per translated name/description
        """
        CREATE TRIGGER spell_after_insert
            AFTER INSERT ON spell
        BEGIN
            INSERT INTO spell_search_index (spell_id, language, name, description) VALUES (
                new.id,
                'en',
                new.name,
                new.json_data ->>'$.meta.description'
            );
            INSERT INTO spell_search_index (spell_id, language, name, description)
                SELECT
                    new.id,
                    json_each.key,
                    json_each.value ->> '$.name',
                    json_each.value ->> '$.description'
                FROM json_each(new.json_data ->> '$.meta.translations');
        END;
        """,
        # Populate the search index with the existing spells
        """
        INSERT INTO spell_search_index (spell_id, language, name, description)
            SELECT
                id,
                'en',
                name,
                json_data ->> '$.meta.description'
            FROM spell;
        """,
        """
        INSERT INTO spell_search_index (spell_id, language, name, description)
            SELECT
                spell.id,
                json_each.key,
                json_each.value ->> '$.name',
                json_each.value ->> '$.description'
            FROM spell, json_each(spell.json_data ->> '$.meta.translations');
        """,
        # Every time an spell is deleted from DB, delete it from the search index
        """
        CREATE TRIGGER spell_after_delete
            AFTER DELETE ON spell
        BEGIN
            DELETE FROM spell_search_index WHERE spell_id=old.id;
        END;
        """,
        # Every time an spell is update in DB, update it in the search index as well
        """
        CREATE TRIGGER spell_after_update
            AFTER UPDATE ON spell
            WHEN old.name <> new.name
                OR old.json_data <> new.json_data
        BEGIN
            REPLACE INTO spell_search_index (spell_id, language, name, description) VALUES (
                new.id,
                'en',
                new.name,
                new.json_data ->> '$.meta.description'
            );
            REPLACE INTO spell_search_index (spell_id, language, name, description)
                SELECT
                    new.id,
                    json_each.key,
                    json_each.value ->> '$.name',
                    json_each.value ->> '$.description'
                FROM json_each(new.json_data ->> '$.meta.translations');
        END
        """,
    ]
    for stmt in ddls:
        op.execute(stmt)


def downgrade() -> None:
    ddls = [
        "DROP TRIGGER spell_after_update",
        "DROP TRIGGER spell_after_delete",
        "DROP TRIGGER spell_after_insert",
        "DROP TABLE spell_search_index",
    ]
    for stmt in ddls:
        op.execute(stmt)
