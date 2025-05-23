"""added skill table

Revision ID: f110a597acd9
Revises: create_users_table
Create Date: 2025-05-12 08:50:27.073296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'f110a597acd9'
down_revision: Union[str, None] = 'create_users_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('is_active', mysql.BOOLEAN(), nullable=False, server_default='1'),
    sa.Column('first_name', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('birth_date', mysql.DATE(), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'users', ['email'], unique=True)
    
    op.create_table('skills',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', mysql.INTEGER(), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=256), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skills')
    op.drop_index('email', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
