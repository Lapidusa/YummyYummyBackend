import uuid
from uuid import UUID

from pydantic import BaseModel, Field


class City(BaseModel):

  name: str = Field(..., description="Название города")  # Название города

  class Config:
    from_attributes = True

class CityCreate(City):
  pass

class CityUpdate(City):
  id: UUID = Field(..., description="Уникальный идентификатор города")  # Уникальный идентификатор города
  pass