"""phase 1 — mentee selection pipeline

Adds the disadvantage-score / system-decision / admin-decision columns to
applications, a selection threshold to cohorts, and the application_reviews and
notification_logs tables.

Revision ID: a1b2c3d4e5f6
Revises: dc72e8ae40ae
Create Date: 2026-07-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "dc72e8ae40ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("disadvantage_score", sa.Float(), nullable=False, server_default="0")
        )
        batch_op.add_column(sa.Column("system_decision", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("admin_decision", sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column("admin_decision_notes", sa.Text(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            )
        )

    with op.batch_alter_table("cohorts", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("selection_threshold", sa.Float(), nullable=False, server_default="0")
        )

    op.create_table(
        "application_reviews",
        sa.Column("application_id", sa.Uuid(), nullable=False),
        sa.Column("reviewer_id", sa.Uuid(), nullable=True),
        sa.Column("decision", sa.String(length=20), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("round", sa.Integer(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["reviewer_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "notification_logs",
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("application_id", sa.Uuid(), nullable=True),
        sa.Column("channel", sa.String(length=20), nullable=False),
        sa.Column("template", sa.String(length=50), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["application_id"], ["applications.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("notification_logs")
    op.drop_table("application_reviews")
    with op.batch_alter_table("cohorts", schema=None) as batch_op:
        batch_op.drop_column("selection_threshold")
    with op.batch_alter_table("applications", schema=None) as batch_op:
        batch_op.drop_column("created_at")
        batch_op.drop_column("admin_decision_notes")
        batch_op.drop_column("admin_decision")
        batch_op.drop_column("system_decision")
        batch_op.drop_column("disadvantage_score")
