from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import create_profile, get_profile, get_profiles, update_profile, delete_profile
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from typing import List

router = APIRouter()

# 🔹 Crear un nuevo perfil
@router.post("/profiles/", response_model=ProfileResponse)
def create_new_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    return create_profile(db, profile)

# 🔹 Obtener un perfil por ID
@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
def read_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile

# 🔹 Obtener todos los perfiles
@router.get("/profiles/", response_model=List[ProfileResponse])
def read_profiles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_profiles(db, skip, limit)

# 🔹 Actualizar un perfil
@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_existing_profile(profile_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    updated_profile = update_profile(db, profile_id, profile)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return updated_profile

# 🔹 Eliminar un perfil
@router.delete("/profiles/{profile_id}")
def delete_existing_profile(profile_id: int, db: Session = Depends(get_db)):
    deleted_profile = delete_profile(db, profile_id)
    if not deleted_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"message": "Perfil eliminado"}
