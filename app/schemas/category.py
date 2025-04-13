from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

# Pydantic-схема для отображения категории
class Category(BaseModel):
  id: UUID = Field(..., description="Уникальный идентификатор категории")
  name: str = Field(..., description="Название категории")
  store_ids: List[UUID] = Field(default=[], description="Список идентификаторов магазинов, связанных с категорией")
  product_ids: List[UUID] = Field(default=[], description="Список идентификаторов продуктов, связанных с категорией")
  is_available: Optional[bool] = Field(None, description="Доступна ли категория")
  type: str = Field(..., description="Тип категории")
  class Config:
    from_attributes  = True

class CreateCategory(BaseModel):
  name: str = Field(..., description="Название категории")
  store_id: Optional[UUID] = Field(None, description="Идентификатор магазина, к которому относится категория")
  is_available: Optional[bool] = Field(None, description="Доступна ли категория")
  type: str = Field(..., description="Тип категории")

class UpdateCategory(BaseModel):
  id: UUID = Field(..., description="Уникальный идентификатор категории")
  name: Optional[str] = Field(None, description="Новое название категории")
  store_id: Optional[UUID] = Field(None, description="Новый идентификатор магазина, связанного с категорией")
  is_available: Optional[bool] = Field(None, description="Доступна ли категория")
  type: str = Field(..., description="Тип категории")