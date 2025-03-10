from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# 🔹 Esquema para crear un perfil
class ProfileCreate(BaseModel):
    name: str
    email: EmailStr
    specialty: str
    linkedin: Optional[str] = None

# 🔹 Esquema para actualizar un perfil
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    specialty: Optional[str] = None
    linkedin: Optional[str] = None
    status: Optional[str] = None

# 🔹 Esquema para mostrar un perfil
class ProfileResponse(ProfileCreate):
    id: int
    status: str
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True
