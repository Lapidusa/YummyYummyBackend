import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from fastapi import HTTPException, APIRouter
from sqlalchemy import select

from app.core.config import settings
TOKEN_BLACKLIST = set()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class SecurityMiddleware:
  @staticmethod
  async def generate_jwt_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token

  @staticmethod
  async def get_current_user(token: str, db: AsyncSession):
    # Проверяем, находится ли токен в черном списке
    if token in TOKEN_BLACKLIST:
      raise HTTPException(status_code=401, detail="Токен отозван")

    try:
      payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
      user_id = payload.get("user_id")
      if user_id is None:
        raise HTTPException(status_code=401, detail="Недействительный токен")

      # Проверяем, существует ли пользователь
      async with db as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
          raise HTTPException(status_code=401, detail="Пользователь не найден")
    except jwt.PyJWTError:
      raise HTTPException(status_code=401, detail="Недействительный токен")
    return user

  @staticmethod
  async def logout(token: str):
    TOKEN_BLACKLIST.add(token)
    return {"message": "Токен успешно отозван"}