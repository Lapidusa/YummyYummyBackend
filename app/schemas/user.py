from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Roles(str, Enum):
  USER = 0
  ADMIN = 1
  COURIER = 2
  MANAGER = 3

class UserBase(BaseModel):
    phone_number: str = Field(..., max_length=15)
    email: Optional[EmailStr]
    name: Optional[str]
    date_of_birth: Optional[datetime]
    role: Roles = Roles.USER
    image_url: Optional[str]
    scores: Optional[int]
