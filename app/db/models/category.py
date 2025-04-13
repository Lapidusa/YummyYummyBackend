import uuid
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import Column, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.db.models.product import product_categories

store_categories = Table(
    'store_categories',
    Base.metadata,
    Column('store_id', UUID(as_uuid=True), ForeignKey('stores.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)
)
class TypeCategory(PyEnum):
  GROUP = "group"
  PIZZA = "pizza"
  CONSTRUCTOR = "constructor"

class Category(Base):
  __tablename__ = 'categories'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(255), nullable=False)
  store_id = Column(UUID(as_uuid=True), ForeignKey('stores.id'))
  is_available = Column(Boolean, nullable=False, default=True)
  type = Column(ENUM(TypeCategory), default=TypeCategory.GROUP, nullable=False)
  stores = relationship("Store", secondary=store_categories, back_populates="categories")
  products = relationship("Product", secondary=product_categories, back_populates="categories")