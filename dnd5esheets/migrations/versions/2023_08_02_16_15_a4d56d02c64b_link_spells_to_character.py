"""link_spells_to_character

Revision ID: a4d56d02c64b
Revises: d4d2b2fce5f8
Create Date: 2023-08-02 16:15:35.356745

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a4d56d02c64b"
down_revision = "d4d2b2fce5f8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "known_spell",
        sa.Column("prepared", sa.Boolean(), nullable=False),
        sa.Column("spell_id", sa.Integer(), nullable=False),
        sa.Column("character_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["character_id"],
            ["character.id"],
        ),
        sa.ForeignKeyConstraint(
            ["spell_id"],
            ["spell.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("known_spell", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_known_spell_created_at"), ["created_at"], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("known_spell", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_known_spell_created_at"))

    op.drop_table("known_spell")
    # ### end Alembic commands ###
