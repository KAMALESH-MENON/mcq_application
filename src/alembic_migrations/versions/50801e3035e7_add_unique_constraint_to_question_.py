"""Add unique constraint to question column in mcqs table

Revision ID: 50801e3035e7
Revises: 96cd159c6b79
Create Date: 2025-01-16 09:34:29.417782

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "50801e3035e7"
down_revision: Union[str, None] = "96cd159c6b79"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adding a unique constraint to the question column
    op.create_unique_constraint("uq_mcqs_question", "mcqs", ["question"])


def downgrade() -> None:
    # Dropping the unique constraint in case of a rollback
    op.drop_constraint("uq_mcqs_question", "mcqs", type_="unique")
