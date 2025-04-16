from fastapi import Header, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime

from app.core.security import SecurityMiddleware
from app.db.base import get_db
from app.db.models.user import User, Roles
from app.services.responsive import ResponseUtils


class UserService:


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

  async def get_user_by_phone(db: AsyncSession, phone: str):
    return await db.execute(select(User).where(User.phone_number == phone))