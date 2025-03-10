from sqlalchemy.orm import Session
from models import Profile, ProfileHistory, ProfileStatus
from schemas import ProfileCreate, ProfileUpdate
from datetime import datetime

# 🔹 Crear un nuevo perfil
def create_profile(db: Session, profile_data: ProfileCreate):
    profile = Profile(**profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Guardar historial de estado
    history = ProfileHistory(profile_id=profile.id, status=profile.status)
    db.add(history)
    db.commit()

    return profile

# 🔹 Obtener un perfil por ID
def get_profile(db: Session, profile_id: int):
    return db.query(Profile).filter(Profile.id == profile_id).first()

# 🔹 Obtener todos los perfiles
def get_profiles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Profile).offset(skip).limit(limit).all()

# 🔹 Actualizar perfil
def update_profile(db: Session, profile_id: int, profile_data: ProfileUpdate):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        return None

    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    # Guardar historial de estado si cambió
    if "status" in profile_data.dict():
        history = ProfileHistory(profile_id=profile.id, status=profile.status)
        db.add(history)
        db.commit()

    return profile

# 🔹 Eliminar perfil
def delete_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if profile:
        db.delete(profile)
        db.commit()
    return profile
