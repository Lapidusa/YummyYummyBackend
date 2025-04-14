import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class City(Base):
    __tablename__ = 'cities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)  # Название зоны (например, "Запад")
    stores = relationship("Store", back_populates="city")
