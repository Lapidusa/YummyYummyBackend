import os
import logging
from typing import Optional
from datetime import datetime, timedelta
import asyncio
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.db.models import User
from app.db.models.user import Roles
from app.routers.user import router as user_router
from app.routers.store import router as store_router
from app.routers.category import router as category_router
from app.routers.city import router as city_router
from app.core.config import settings
from dotenv import load_dotenv, find_dotenv
import uvicorn

# Настройки
load_dotenv(find_dotenv())
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

DATABASE_URL = settings.DATABASE_URL
ADMIN_PHONE = settings.ADMIN_PHONE

# Настройка асинхронного движка SQLAlchemy
engine = create_async_engine(DATABASE_URL, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Главный роутер
app = FastAPI(default_response_class=ORJSONResponse)

# Мультитерриториальная политика
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роуты
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(city_router, prefix="/city", tags=["City"])
app.include_router(store_router, prefix="/store", tags=["Store"])
app.include_router(category_router, prefix="/category", tags=["Category"])

# Основная точка входа
@app.get("/", include_in_schema=False)
def read_root():
    return {"message": "This is a backend service for Yummy Yummy!"}

# # Лифспэн события (начало / конец приложения)
# @app.router.lifespan
# async def lifespan(app: FastAPI):
#     logger.info("Initializing database connection...")
#     async with engine.begin() as conn:
#         await conn.run_sync(create_all_tables)
#     yield
#     logger.info("Closing database connection...")
#     await engine.dispose()

# Вспомогательная функция для создания администратора
async def create_admin(session: AsyncSession):
    result = await session.execute(select(User).filter(User.phone_number == ADMIN_PHONE))
    admin = result.scalars().first()
    if not admin:
        admin = User(phone_number=ADMIN_PHONE, role=Roles.ADMIN)
        session.add(admin)
        await session.commit()
        logger.info(f"Admin user created with phone number: {ADMIN_PHONE}")
    else:
        logger.info(f"Admin user already exists with phone number: {ADMIN_PHONE}")

# # Выполнение при старте приложения
# @app.on_startup
# async def startup():
#     async with SessionLocal() as session:
#         await create_admin(session)

# Запуск приложения
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)