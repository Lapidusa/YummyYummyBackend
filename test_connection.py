from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
import asyncio
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

async def test_connection():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        await conn.commit()  # Явный COMMIT
        print("Transaction committed.")

if __name__ == "__main__":
    asyncio.run(test_connection())