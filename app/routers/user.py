import logging

import redis
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.responsive import ResponseUtils
from app.services.sms_service import SmsService
from app.services.user_service import UserService
from app.core.security import SecurityMiddleware
from sqlalchemy import select
from app.db.models.user import User
from pydantic import BaseModel
from app.db.base import get_db

sms_service = SmsService()
router = APIRouter()
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
class RegisterOrLoginRequest(BaseModel):
  phone_number: str

class VerifyCodeRequest(BaseModel):
  phone_number: str
  code: str

logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)
@router.post("/send-sms/")
async def send_sms(request: RegisterOrLoginRequest):
  print("sdasdsadsad")
  logger.info("ААААААААААААААААА")
  response = await sms_service.send_sms(request.phone_number)

  if response is None:
    raise ResponseUtils.error(message="Ошибка при отправке SMS")

  return ResponseUtils.success(message="SMS отправлен успешно")


# Обработчик проверки кода подтверждения
@router.post("/verify-code/")
async def verify_code(request: VerifyCodeRequest, db: AsyncSession = Depends(get_db)):

  stored_code = redis_client.get(request.phone_number)

  if stored_code and stored_code.decode('utf-8') == request.code:
    await redis_client.delete(request.phone_number)

    existing_user = await UserService.get_user_by_phone(db, request.phone_number)

    if existing_user:
      token = await SecurityMiddleware.generate_jwt_token(str(existing_user.id))

      return ResponseUtils.success(
        token=token,
        user={
          "id": existing_user.id,
          "phone_number": existing_user.phone_number
        },
        message="Авторизация прошла успешно"
      )
    else:
      # Новый пользователь, создаём запись
      new_user = await UserService.create_new_user(db, request.phone_number)
      token = await SecurityMiddleware.generate_jwt_token(str(new_user.id))

      return ResponseUtils.success(
        token=token,
        user={
          "id": new_user.id,
          "phone_number": new_user.phone_number
        },
        message="Новый пользователь зарегистрирован успешно"
      )
  else:
    raise ResponseUtils.error(message="Неверный код или срок действия кода истёк")
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
