from fastapi import APIRouter, Depends, HTTPException
from app.api.profile_api import ProfileApi
from app.api.profile_schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from app.config.dependencies import get_profile_api
from typing import List

router = APIRouter()


# 🔹 Crear un nuevo perfil
@router.post("/profiles/", response_model=ProfileResponse)
def create_new_profile(profile: ProfileCreate, profile_service: ProfileApi = Depends(get_profile_api)):
    return profile_service.create_profile(
        name=profile.name,
        email=profile.email,
        specialty=profile.specialty,
        linkedin=profile.linkedin,
    )


# 🔹 Obtener un perfil por ID
@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
def read_profile(profile_id: int, profile_service: ProfileApi = Depends(get_profile_api)):
    profile = profile_service.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return profile


# 🔹 Obtener todos los perfiles
@router.get("/profiles/", response_model=List[ProfileResponse])
def read_profiles(skip: int = 0, limit: int = 10, profile_service: ProfileApi = Depends(get_profile_api)):
    return profile_service.get_profiles(skip, limit)


# 🔹 Actualizar un perfil
@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_existing_profile(profile_id: int, profile: ProfileUpdate, profile_service: ProfileApi = Depends(get_profile_api)):
    updated_profile = profile_service.update_profile(
        profile_id=profile_id,
        name=profile.name,
        email=profile.email,
        specialty=profile.specialty,
        linkedin=profile.linkedin,
        status=profile.status,
    )
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return updated_profile


# 🔹 Eliminar un perfil
@router.delete("/profiles/{profile_id}")
def delete_existing_profile(profile_id: int, profile_service: ProfileApi = Depends(get_profile_api)):
    deleted_profile = profile_service.delete_profile(profile_id)
    if not deleted_profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return {"message": "Perfil eliminado"}
