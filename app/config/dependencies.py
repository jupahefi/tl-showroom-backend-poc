from app.db.profile_repository import ProfileRepository as ProfileRepositoryImpl
from app.api.profile_api import ProfileApi
from app.services.profile_service import ProfileService
from app.config.database import get_db
from fastapi import Depends
from typing import Any

def get_profile_repository(db: Any) -> ProfileRepositoryImpl:
    """
    Factory function that returns a profile repository implementation.
    This hides the SQLAlchemy dependency from the routes.
    """
    return ProfileRepositoryImpl(db)

def get_profile_service(db: Any = Depends(get_db)) -> ProfileService:
    """
    Factory function that returns a ProfileService.
    This hides the repository dependency from the API.
    """
    repository = get_profile_repository(db)
    return ProfileService(repository)

def get_profile_api(profile_service: ProfileService = Depends(get_profile_service)) -> ProfileApi:
    """
    Factory function that returns a ProfileApi.
    This hides the service dependency from the routes.
    """
    return ProfileApi(profile_service)
