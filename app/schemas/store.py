from pydantic import BaseModel, Field
from typing import List
from datetime import time
from uuid import UUID

from app.schemas.category import Category
from app.schemas.city import City

class Store(BaseModel):
  id: UUID = Field(..., description="Уникальный идентификатор магазина")  # Уникальный идентификатор магазина
  address: str = Field(..., description="Адрес магазина")  # Адрес магазина
  start_working_hours: time = Field(..., description="Начало рабочего времени")  # Время начала работы
  end_working_hours: time = Field(..., description="Конец рабочего времени")  # Время окончания работы
  start_delivery_time: time = Field(..., description="Начало времени доставки")  # Время начала доставки
  end_delivery_time: time = Field(..., description="Конец времени доставки")  # Время окончания доставки
  phone_number: str = Field(..., description="Номер телефона магазина")  # Номер телефона
  categories: List[Category] = Field(default_factory=list, description="Список связанных категорий")  # Связанные категории
  city: City = Field(..., description="Город, к которому принадлежит магазин")  # Город, связанный с магазином

  class Config:
    from_attributes = True

class CreateStore(BaseModel):
  address: str
  start_working_hours: time
  end_working_hours: time
  start_delivery_time: time
  end_delivery_time: time
  phone_number: str

class UpdateStore(BaseModel):
  id: UUID
  address: str
  start_working_hours: time
  end_working_hours: time
  start_delivery_time: time
  end_delivery_time: time
  phone_number: str
