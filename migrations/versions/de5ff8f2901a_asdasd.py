"""asdasd

Revision ID: de5ff8f2901a
Revises: dc2040016adb
Create Date: 2025-03-05 19:14:03.826928

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'de5ff8f2901a'
down_revision: Union[str, None] = 'dc2040016adb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем ENUM тип typecategory
    type_category_enum = postgresql.ENUM('GROUP', 'PIZZA', 'CONSTRUCTOR', name='typecategory')
    type_category_enum.create(op.get_bind(), checkfirst=True)

    # Изменяем колонку type в таблице categories, используя выражение USING
    op.execute(
        """
        ALTER TABLE categories
        ALTER COLUMN type TYPE typecategory
        USING type::typecategory
        """
    )

    # Изменяем колонку address в таблице stores
    op.alter_column(
        'stores',
        'address',
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=500),
        existing_nullable=False
    )


def downgrade() -> None:
    # Удаляем изменения в таблице stores
    op.alter_column(
        'stores',
        'address',
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False
    )

    # Удаляем изменения в таблице categories
    op.execute(
        """
        ALTER TABLE categories
        ALTER COLUMN type TYPE VARCHAR(255)
        USING type::VARCHAR
        """
    )

    # Удаляем ENUM тип typecategory
    type_category_enum = postgresql.ENUM('GROUP', 'PIZZA', 'CONSTRUCTOR', name='typecategory')
    type_category_enum.drop(op.get_bind(), checkfirst=True)