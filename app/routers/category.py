from uuid import UUID

from fastapi import APIRouter, Depends, Header
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import SecurityMiddleware
from app.db.base import get_db
from app.schemas.category import CreateCategory, UpdateCategory
from app.services.responsive import ResponseUtils
from app.services.category_service import CategoryService

router = APIRouter()
@router.get("/{category_id}")
async def get_category_endpoint (
  category_id: UUID,
  db: AsyncSession = Depends(get_db),
):
  try:
    category = await CategoryService.get_category_by_id(db, category_id)
    return ResponseUtils.success(data=category)
  except NoResultFound:
    raise ResponseUtils.error(message="Нет найденной категории")

@router.get("/all-categories/")
async def get_all_stores_endpoint(db: AsyncSession = Depends(get_db)):
  categories = await CategoryService.get_all_categories(db)
  return ResponseUtils.success(categories=categories)
@router.post("/")
async def create_category(
  category_data: CreateCategory,
  db: AsyncSession = Depends(get_db),
  token: str = Header(None)
):
  if token is None:
    raise ResponseUtils.error(message="Токен не предоставлен")
  await SecurityMiddleware.is_admin_or_manager(token, db)
  try:
    new_category = await CategoryService.create_category(db, category_data)
    return ResponseUtils.success(data=new_category, message="Категория создана")
  except Exception as e:
    raise ResponseUtils.error(message=str(e))

@router.put("/")
async def update_category(
  category_data: UpdateCategory,
  db: AsyncSession = Depends(get_db),
  token: str = Header(None)
):
  if token is None:
    raise ResponseUtils.error(message="Токен не предоставлен")
  await SecurityMiddleware.is_admin_or_manager(token, db)
  try:
    updated_category = await CategoryService.update_category(db, category_data)
    return ResponseUtils.success(data=updated_category, message="Категория успешно изменена")
  except Exception as e:
    raise ResponseUtils.error(message=str(e))

@router.delete("/{category_id}")
async def delete_category_endpoint(
  category_id: UUID,
  db: AsyncSession = Depends(get_db),
  token: str = Header(None)
):
  if token is None:
    raise ResponseUtils.error(message="Токен не предоставлен")
  await SecurityMiddleware.is_admin_or_manager(token, db)
  try:
    await CategoryService.delete_category(db, category_id)
    return ResponseUtils.success(message="Категория удалена")
  except NoResultFound:
    raise ResponseUtils.error(message=f"Категория не найдена с Id:{category_id}")