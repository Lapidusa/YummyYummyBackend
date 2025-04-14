from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.responsive import ResponseUtils
from app.services.sms_service import SmsService
from app.services.user_service import UserService
from app.core.security import SecurityMiddleware
from sqlalchemy import select
from app.db.models.user import User
from pydantic import BaseModel
from app.db.base import get_db

sms_service = SmsService()
router = APIRouter()

class RegisterOrLoginRequest(BaseModel):
  phone_number: str

class VerifyCodeRequest(BaseModel):
  phone_number: str
  code: str

@router.post("/send-sms/")
async def send_sms(request: RegisterOrLoginRequest):
  response = await sms_service.send_sms(request.phone_number)
  if response is None:
    return ResponseUtils.error(message="Ошибка при отправке SMS")
  return ResponseUtils.success(message="SMS отправлено успешно")
@router.post("/verify-code/")
async def verify_code(request: VerifyCodeRequest, db: AsyncSession = Depends(get_db)):
  sms_code = sms_service.get_sms_code(request.phone_number)
  if sms_code and sms_code.is_valid(request.code):
    sms_service.delete_sms_code(request.phone_number)

    if not await UserService.check_users(db):
      new_user = await UserService.create_new_user(db, request.phone_number)
      token = await SecurityMiddleware.generate_jwt_token(str(new_user.id))
      return ResponseUtils.success(token = token, user = new_user)

    result = await db.execute(select(User).where(User.phone_number == request.phone_number))
    user = result.scalar_one_or_none()

    if user:
      token = await SecurityMiddleware.generate_jwt_token(str(user.id))
      return ResponseUtils.success(token = token, user = user)
    else:
      new_user = await UserService.create_new_user(db, request.phone_number)
      token = await SecurityMiddleware.generate_jwt_token(str(new_user.id))
      return ResponseUtils.success(token = token, user = new_user)
  return ResponseUtils.error(message="Неверный код или код истек")

@router.get("/get-user/")
async def get_user(token: str = Header(alias="token"), db: AsyncSession = Depends(get_db)):
  user = await SecurityMiddleware.get_current_user(token, db)
  if user:
    return ResponseUtils.success(user=user)
  else:
    return ResponseUtils.error(message="Не найден пользователь")

@router.post("/logout/")
async def logout_route(token: str = Header(alias="token"), db: AsyncSession = Depends(get_db)):
  user = await SecurityMiddleware.get_current_user(token, db)
  if user:
    await SecurityMiddleware.logout(token)
    return ResponseUtils.success(message="Вы успешно вышли из системы")
  else:
    return ResponseUtils.error(message="Не действительный токен")
