from sqlalchemy import Column, String, Float, ForeignKey, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, ENUM
from sqlalchemy.orm import relationship, declared_attr
import uuid
from enum import Enum as PyEnum
from app.db.base import Base
from app.db.models.ingredient import product_ingredients

product_categories = Table(
    'product_categories',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)
)

class Type(PyEnum):
  GROUP = 0
  CONSTRUCTOR = 1
  PIZZA = 2


class Product(Base):
  __tablename__ = 'products'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  name = Column(String(255), nullable=False)  # Название продукта
  description = Column(String(500), nullable=True)  # Описание продукта
  is_available = Column(Boolean, nullable=False, default=True)  # Доступность продукта
  type = Column(ENUM(Type), default=Type.GROUP, nullable=False)  # Тип продукта
  categories = relationship("Category", secondary=product_categories, back_populates="products")
  variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")

class ProductVariant(Base):
  __tablename__ = 'product_variants'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)  # Связь с продуктом
  size = Column(String(50), nullable=False)  # Размер варианта (например, "3 шт", "6 шт", "9 шт")
  price = Column(Float, nullable=False)  # Цена варианта
  weight = Column(Float, nullable=True)  # Вес варианта (в граммах)
  calories = Column(Float, nullable=True)  # Калории
  proteins = Column(Float, nullable=True)  # Белки
  fats = Column(Float, nullable=True)  # Жиры
  carbohydrates = Column(Float, nullable=True)  # Углеводы
  is_available = Column(Boolean, nullable=False, default=True)  # Доступность варианта

  # Связь с продуктом
  product = relationship("Product", back_populates="variants")

class Dough(PyEnum):
  THICK_DOUGH = 0 # толстое тесто
  THIN_DOUGH = 1 # тонкое тесто


class Pizza(Product):
  __tablename__ = 'pizzas'

  id = Column(UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True)
  ingredients = relationship("Ingredient", secondary=product_ingredients, back_populates="products")
  dough = Column(ENUM(Dough, name="dough", create_type=True), default=Dough.THICK_DOUGH, nullable=False)

  __mapper_args__ = {
    'polymorphic_identity': 'pizza',  # Указываем идентификатор для полиморфизма
  }
