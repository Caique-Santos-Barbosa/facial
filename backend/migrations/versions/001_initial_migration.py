"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-12 20:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create employees table
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('position', sa.String(length=100), nullable=True),
        sa.Column('face_encoding', sa.LargeBinary(), nullable=False),
        sa.Column('face_image_path', sa.String(length=500), nullable=False),
        sa.Column('face_registered_at', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_employees_id'), 'employees', ['id'], unique=False)
    op.create_index(op.f('ix_employees_full_name'), 'employees', ['full_name'], unique=False)
    op.create_index(op.f('ix_employees_cpf'), 'employees', ['cpf'], unique=True)
    op.create_index(op.f('ix_employees_email'), 'employees', ['email'], unique=True)
    op.create_index(op.f('ix_employees_is_active'), 'employees', ['is_active'], unique=False)
    
    # Create access_logs table
    op.create_table(
        'access_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=True),
        sa.Column('access_granted', sa.Boolean(), nullable=False),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('liveness_passed', sa.Boolean(), nullable=True),
        sa.Column('attempted_at', sa.DateTime(), nullable=True),
        sa.Column('device_id', sa.String(length=100), nullable=True),
        sa.Column('device_location', sa.String(length=255), nullable=True),
        sa.Column('capture_image_path', sa.String(length=500), nullable=True),
        sa.Column('denial_reason', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_logs_id'), 'access_logs', ['id'], unique=False)
    op.create_index(op.f('ix_access_logs_attempted_at'), 'access_logs', ['attempted_at'], unique=False)
    op.create_index(op.f('ix_access_logs_access_granted'), 'access_logs', ['access_granted'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_access_logs_access_granted'), table_name='access_logs')
    op.drop_index(op.f('ix_access_logs_attempted_at'), table_name='access_logs')
    op.drop_index(op.f('ix_access_logs_id'), table_name='access_logs')
    op.drop_table('access_logs')
    op.drop_index(op.f('ix_employees_is_active'), table_name='employees')
    op.drop_index(op.f('ix_employees_email'), table_name='employees')
    op.drop_index(op.f('ix_employees_cpf'), table_name='employees')
    op.drop_index(op.f('ix_employees_full_name'), table_name='employees')
    op.drop_index(op.f('ix_employees_id'), table_name='employees')
    op.drop_table('employees')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
