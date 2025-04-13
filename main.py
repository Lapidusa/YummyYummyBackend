import ssl

from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.store import router as store_router
from app.routers.category import router as category_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
import uvicorn
import os
app = FastAPI()
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
app.include_router(store_router, prefix="/store", tags=["Store"])
app.include_router(category_router, prefix="/category", tags=["Category"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.100", port=8080, reload=True)