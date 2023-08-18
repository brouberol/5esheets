"""associate_player_to_party_role

Revision ID: 4e711ca20c98
Revises: e3f5418ab972
Create Date: 2023-08-17 09:55:23.187731

"""
import sqlalchemy as sa
from alembic import op

from dnd5esheets.models import Role, SqliteStrEnum

# revision identifiers, used by Alembic.
revision = "4e711ca20c98"
down_revision = "e3f5418ab972"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "player_role",
        sa.Column("role", SqliteStrEnum(Role), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("party_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["party_id"],
            ["party.id"],
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "party_id", "player_id", name="party_id_unique_per_player_id"
        ),
    )
    with op.batch_alter_table("player_role", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_player_role_created_at"), ["created_at"], unique=False
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("player_role", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_player_role_created_at"))

    op.drop_table("player_role")
    # ### end Alembic commands ###