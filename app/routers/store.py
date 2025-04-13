from fastapi import Depends, APIRouter
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.db.base import get_db
from app.schemas.responsive import ResponseUtils
from app.schemas.store import CreateStore, UpdateStore
from app.services.store_service import StoreService
from app.services.user_service import UserService
router = APIRouter()

@router.get("/get-store/{store_id}")
async def get_store_endpoint(store_id: UUID, db: AsyncSession = Depends(get_db)):
  try:
    store = await StoreService.get_store_by_id(db, store_id)
    return ResponseUtils.success(data=store, message="Магазин успешно создан")
  except NoResultFound:
    raise ResponseUtils.error(message="Нет найденного магазина")

@router.get("/all-stores/")
async def get_all_stores_endpoint(db: AsyncSession = Depends(get_db)):
  stores = await StoreService.get_all_stores(db)
  return stores

@router.post("/create-store/")
async def create_store_endpoint(
  store_data: CreateStore,
  db: AsyncSession = Depends(get_db),
  token: str = Depends(UserService.validate_user_role)
):
  if not token.get("result"):
    return ResponseUtils.error(message=token.get("message"))
  try:
    new_store = await StoreService.create_store(db, store_data)
    return ResponseUtils.success(data=new_store, message="Магазин успешно создан")
  except IntegrityError as e:
    if "stores_phone_number_key" in str(e.orig):
      return ResponseUtils.error(message="Магазин с таким номером телефона уже существует.")
    return ResponseUtils.error(message="Произошла ошибка при создании магазина.")
  except Exception as e:
    return ResponseUtils.error(message=str(e))

@router.put("/{store_id}")
async def update_store_endpoint(
  store_data: UpdateStore,
  db: AsyncSession = Depends(get_db),
  token: str = Depends(UserService.validate_user_role)
):
  if not token.get("result"):
    return token
  try:
    updated_store = await StoreService.update_store(db, store_data)
    return ResponseUtils.success(data=updated_store, message="Магазин успешно изменен")
  except NoResultFound:
    raise ResponseUtils.error(message="Магазин не найден")
  except IntegrityError as e:
    if "stores_phone_number_key" in str(e.orig):
      return ResponseUtils.error(message="Магазин с таким номером телефона уже существует.")
    return ResponseUtils.error(message="Произошла ошибка при изменении магазина.")
  except Exception as e:
    return ResponseUtils.error(message=str(e))

@router.delete("/stores/{store_id}")
async def delete_store_endpoint(
  store_id: UUID,
  db: AsyncSession = Depends(get_db),
  token: str = Depends(UserService.validate_user_role)
):
  if not token.get("result"):
    return token
  try:
    await StoreService.delete_store(db, store_id)
    return ResponseUtils.success(message="Магазин удален")
  except NoResultFound:
    raise ResponseUtils.error(message="Магазин не найден")