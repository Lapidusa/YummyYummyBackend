import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

# Промежуточная таблица для связи "многие ко многим" между продуктами и ингредиентами
product_ingredients = Table(
    'product_ingredients',
    Base.metadata,
    Column('product_id', UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True),
    Column('ingredient_id', UUID(as_uuid=True), ForeignKey('ingredients.id'), primary_key=True)
)

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # Название ингредиента
    is_removable = Column(Boolean, nullable=False, default=True)  # Можно ли удалить ингредиент из состава

    # Связь с продуктами
    products = relationship("Product", secondary=product_ingredients, back_populates="ingredients")