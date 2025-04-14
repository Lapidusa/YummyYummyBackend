from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import User
from app.db.models.user import Roles
from app.routers.user import router as user_router
from app.routers.store import router as store_router
from app.routers.category import router as category_router
from app.routers.city import router as city_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings  # Импортируйте настройки
import uvicorn
import ssl

# Создание асинхронного движка
DATABASE_URL = settings.DATABASE_URL  # Убедитесь, что у вас есть URL базы данных в настройках
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронного sessionmaker
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()
ADMIN_PHONE = settings.ADMIN_PHONE  # Используйте переменную из настроек

async def create_admin(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(User).where(User.phone_number == ADMIN_PHONE))
        admin = result.scalars().first()
        if not admin:
            admin = User(phone_number=ADMIN_PHONE, role=Roles.ADMIN)
            db.add(admin)
            await db.commit()

# Использование lifespan для управления событиями
@app.on_event("startup")
async def startup_event():
    async with SessionLocal() as db:
        await create_admin(db)

# Настройка CORS и SSL
origins = [
    "http://localhost:3000",
]
certfile = r"C:\Users\user\server.crt"
keyfile = r"C:\Users\user\server.key"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

@app.get("/")
async def root():
    return {"message": "Это сервер приложения Yummy Yummy!"}

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(city_router, prefix="/city", tags=["City"])
app.include_router(store_router, prefix="/store", tags=["Store"])
app.include_router(category_router, prefix="/category", tags=["Category"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.100", port=8080, reload=True)
