"""phases 2-6 — onboarding, mapping, documents, workshops, close-of-programme

Adds:
  * users: is_alumni, declaration_signed_at
  * mentor_profiles: studied_abroad, discipline, english_support_opt_in
  * mentee_profiles: discipline, mentorship_type, english_support_opt_in
  * new tables: documents, workshops, workshop_signups, programme_feedback,
    offer_records

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-28 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NOW = sa.text("(CURRENT_TIMESTAMP)")


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as b:
        b.add_column(sa.Column("is_alumni", sa.Boolean(), nullable=False, server_default="0"))
        b.add_column(sa.Column("declaration_signed_at", sa.DateTime(timezone=True), nullable=True))

    with op.batch_alter_table("mentor_profiles", schema=None) as b:
        b.add_column(sa.Column("studied_abroad", sa.Boolean(), nullable=False, server_default="0"))
        b.add_column(sa.Column("discipline", sa.String(length=120), nullable=True))
        b.add_column(sa.Column("english_support_opt_in", sa.Boolean(), nullable=False, server_default="0"))

    with op.batch_alter_table("mentee_profiles", schema=None) as b:
        b.add_column(sa.Column("discipline", sa.String(length=120), nullable=True))
        b.add_column(sa.Column("mentorship_type", sa.String(length=20), nullable=True))
        b.add_column(sa.Column("english_support_opt_in", sa.Boolean(), nullable=False, server_default="0"))

    op.create_table(
        "documents",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("cohort_id", sa.Uuid(), nullable=True),
        sa.Column("doc_type", sa.String(length=60), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("reviewer_id", sa.Uuid(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=_NOW, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["cohort_id"], ["cohorts.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reviewer_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "workshops",
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("scheduled_date", sa.Date(), nullable=True),
        sa.Column("recording_url", sa.String(length=500), nullable=True),
        sa.Column("audience", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=_NOW, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "workshop_signups",
        sa.Column("workshop_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=_NOW, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["workshop_id"], ["workshops.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "programme_feedback",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("cohort_id", sa.Uuid(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=_NOW, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["cohort_id"], ["cohorts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "offer_records",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("cohort_id", sa.Uuid(), nullable=True),
        sa.Column("university", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=60), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=_NOW, nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["cohort_id"], ["cohorts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("offer_records")
    op.drop_table("programme_feedback")
    op.drop_table("workshop_signups")
    op.drop_table("workshops")
    op.drop_table("documents")
    with op.batch_alter_table("mentee_profiles", schema=None) as b:
        b.drop_column("english_support_opt_in")
        b.drop_column("mentorship_type")
        b.drop_column("discipline")
    with op.batch_alter_table("mentor_profiles", schema=None) as b:
        b.drop_column("english_support_opt_in")
        b.drop_column("discipline")
        b.drop_column("studied_abroad")
    with op.batch_alter_table("users", schema=None) as b:
        b.drop_column("declaration_signed_at")
        b.drop_column("is_alumni")
