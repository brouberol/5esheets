"""add_created_updated_at_to_all_models

Revision ID: cb612db24d70
Revises: ac918762ed96
Create Date: 2023-06-27 16:51:51.028955

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cb612db24d70"
down_revision = "ac918762ed96"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("character", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f("ix_character_created_at"), ["created_at"], unique=False)

    with op.batch_alter_table("equipped_item", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f("ix_equipped_item_created_at"), ["created_at"], unique=False)

    with op.batch_alter_table("item", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f("ix_item_created_at"), ["created_at"], unique=False)

    with op.batch_alter_table("party", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f("ix_party_created_at"), ["created_at"], unique=False)

    with op.batch_alter_table("player", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False))
        batch_op.create_index(batch_op.f("ix_player_created_at"), ["created_at"], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("player", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_player_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("party", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_party_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("item", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_item_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("equipped_item", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_equipped_item_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    with op.batch_alter_table("character", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_character_created_at"))
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")

    # ### end Alembic commands ###
