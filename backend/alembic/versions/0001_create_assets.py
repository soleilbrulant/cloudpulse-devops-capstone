"""create assets table

Revision ID: 0001_create_assets
Revises: 
Create Date: 2026-10-16 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001_create_assets'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        'assets',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('asset_type', sa.String(length=50), nullable=False),
        sa.Column('provider', sa.String(length=30), nullable=False, server_default='AWS'),
        sa.Column('region', sa.String(length=50), nullable=False, server_default='ap-south-1'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='RUNNING'),
        sa.Column('cost_monthly', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('owner_team', sa.String(length=100), nullable=False, server_default='Platform Engineering'),
        sa.Column('ip_address', sa.String(length=60), nullable=False, server_default='10.0.1.100'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

def downgrade() -> None:
    op.drop_table('assets')
