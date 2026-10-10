"""Added Fee and Fee Structure

Revision ID: 5d19764183be
Revises: ce86c72f69df
Create Date: 2026-09-23 13:31:46.500722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5d19764183be'
down_revision: Union[str, Sequence[str], None] = 'ce86c72f69df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create fee_stucture table
    op.create_table('fee_stucture',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('st_class', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['st_class'], ['student_class.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create fees table
    op.create_table('fees',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('student_id', sa.BigInteger(), nullable=False),
        sa.Column('notes', sa.String(length=255), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('month', sa.Enum('JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', name='months'), nullable=False),
        sa.Column('year', mysql.YEAR(), nullable=False),
        sa.Column('is_paid', sa.Boolean(), nullable=False),
        sa.Column('payment_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fees_student_id'), 'fees', ['student_id'], unique=False)

    # REMOVED: op.drop_constraint, op.drop_index, op.drop_column for student_class 
    # (These were already dropped in MySQL during the partial execution)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_fees_student_id'), table_name='fees')
    op.drop_table('fees')
    op.drop_table('fee_stucture')