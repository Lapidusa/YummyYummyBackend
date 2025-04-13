from typing import List
from uuid import UUID

from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.category import Category, CreateCategory, UpdateCategory
from app.db.models import Category as CategoryModel
from app.schemas.responsive import ResponseUtils

class CategoryService:
  @staticmethod
  async def get_category_by_id(db: AsyncSession, category_id: UUID) -> CategoryModel:
    query = select(CategoryModel).where(CategoryModel.id == category_id)
    result = await db.execute(query)
    category = result.scalar_one_or_none()
    if not category:
      raise NoResultFound(f"Category with ID {category_id} not found")
    return category

  @staticmethod
  async def get_all_categories(db: AsyncSession)->List[Category]:
    query = select(CategoryModel)
    result = await db.execute(query)
    categories = list(result.scalars().all())
    return categories

  @staticmethod
  async def create_category(db: AsyncSession, category_data: CreateCategory) -> Category:
    new_category = CategoryModel(
      name = category_data.name,
      store_id = category_data.store_id,
      is_available = category_data.is_available,
      type = category_data.type
    )
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category

  @staticmethod
  async def update_category(db: AsyncSession, category_data: UpdateCategory) -> Category:
    category = await CategoryService.get_category_by_id(db, category_data.id)
    if not category:
      raise ResponseUtils.error(message="Category with ID {category_data.id} not found")
    category.name = category_data.name
    category.store_id = category_data.store_id
    category.is_available = category_data.is_available
    category.type = category_data.type
    await db.commit()
    await db.refresh(category)
    return category

  @staticmethod
  async def delete_category(db: AsyncSession, category_id: UUID) -> None:
    category = await CategoryService.get_category_by_id(db, category_id)
    if not category:
      raise ResponseUtils.error(message="Category with ID {category_id} not found")
    await db.delete(category)
    await db.commit()
