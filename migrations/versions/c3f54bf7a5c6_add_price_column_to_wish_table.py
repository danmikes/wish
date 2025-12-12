"""Add price column to wish table
Revision ID: c3f54bf7a5c6
Revises:
Create Date: 2025-12-12 13:48:09.422658
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c3f54bf7a5c6'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
  # For SQLite, recreate the table with new column
  op.create_table('wish_new',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
  )

  # Copy all data from old table
  op.execute("""
    INSERT INTO wish_new (id, description, url, image, owner_id, buyer_id, price)
    SELECT id, description, url, image, owner_id, buyer_id, 0.00
    FROM wish
  """)

  # Replace old table with new one
  op.drop_table('wish')
  op.rename_table('wish_new', 'wish')

def downgrade():
  # Recreate table without price column for rollback
  op.create_table('wish_old',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('buyer_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['buyer_id'], ['user.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
  )

  # Copy data back, excluding price column
  op.execute("""
    INSERT INTO wish_old (id, description, url, image, owner_id, buyer_id)
    SELECT id, description, url, image, owner_id, buyer_id
    FROM wish
  """)

  op.drop_table('wish')
  op.rename_table('wish_old', 'wish')
