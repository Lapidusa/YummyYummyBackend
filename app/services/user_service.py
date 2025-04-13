from fastapi import Header, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime

from app.core.security import SecurityMiddleware
from app.db.base import get_db
from app.db.models.user import User, Roles
from app.schemas.responsive import ResponseUtils


class UserService:
  async def validate_user_role(
      token: str = Header(alias="token"),
      db: AsyncSession = Depends(get_db)
  ):
    user = await SecurityMiddleware.get_current_user(token, db)
    if not user:
      return ResponseUtils.error(message="Пользователь не найден")

    if user.role not in [Roles.ADMIN, Roles.MANAGER]:
      return ResponseUtils.error(message="У вас недостаточно прав!")

    return ResponseUtils.success(message="Доступ разрешен")

  async def create_new_user(db: AsyncSession, phone_number: str) -> User:
    new_user = User(
      id = uuid.uuid4(),
      phone_number = phone_number,
      role = Roles.USER,
      created_at = datetime.utcnow(),
      scores = 0
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

  async def check_users(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return len(users) > 0