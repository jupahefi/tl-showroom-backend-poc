from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.config.database import Base
from app.entities import ProfileStatus


# 🔹 Modelo principal de perfiles
class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    specialty = Column(String, nullable=False)
    linkedin = Column(String, nullable=True)
    status = Column(Enum(ProfileStatus), default=ProfileStatus.ACTIVE, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=True)

    # Relación con el historial de estados
    history = relationship("ProfileHistory", back_populates="profile", cascade="all, delete-orphan")


# 🔹 Historial de estados del perfil
class ProfileHistory(Base):
    __tablename__ = "profile_history"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    status = Column(Enum(ProfileStatus), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relación inversa con Profile
    profile = relationship("Profile", back_populates="history")
