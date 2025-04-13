from uuid import UUID

from pydantic import BaseModel, Field


class City(BaseModel):
  id: UUID = Field(..., description="Уникальный идентификатор города")  # Уникальный идентификатор города
  name: str = Field(..., description="Название города")  # Название города

  class Config:
    from_attributes = True

