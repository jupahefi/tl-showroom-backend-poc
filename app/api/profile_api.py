from typing import List, Optional
from app.entities import Profile, ProfileStatus
from app.services.profile_service import ProfileService


class ProfileApi:
    """API for profile-related operations."""

    def __init__(self, profile_service: ProfileService):
        # Use the injected service
        self.profile_service = profile_service

    def create_profile(
        self, name: str, email: str, specialty: str, linkedin: Optional[str] = None
    ) -> Profile:
        """Create a new profile."""
        # Use the service to create and persist the profile
        return self.profile_service.create_profile(name, email, specialty, linkedin)

    def get_profile(self, profile_id: int) -> Optional[Profile]:
        """Get a profile by ID."""
        # Use the service to get the profile
        return self.profile_service.get_profile(profile_id)

    def get_profiles(self, skip: int = 0, limit: int = 10) -> List[Profile]:
        """Get all profiles with pagination."""
        # Use the service to get all profiles
        return self.profile_service.get_profiles(skip, limit)

    def update_profile(
        self,
        profile_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        specialty: Optional[str] = None,
        linkedin: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Optional[Profile]:
        """Update a profile."""
        profile = self.profile_service.get_profile(profile_id)
        if not profile:
            return None

        # Convert status string to enum if provided
        status_enum = None
        if status:
            try:
                # Handle both "inactive" and "INACTIVE" formats
                if status.upper() == "INACTIVE":
                    status_enum = ProfileStatus.INACTIVE
                elif status.upper() == "ACTIVE":
                    status_enum = ProfileStatus.ACTIVE
                elif status.upper() == "SUSPENDED":
                    status_enum = ProfileStatus.SUSPENDED
                elif status.upper() == "DELETED":
                    status_enum = ProfileStatus.DELETED
                else:
                    # Try direct conversion as fallback
                    status_enum = ProfileStatus(status)
            except ValueError:
                # Invalid status value, ignore it
                pass

        # Use the service to update the profile
        return self.profile_service.update_profile(
            profile, name, email, specialty, linkedin, status_enum
        )

    def delete_profile(self, profile_id: int) -> Optional[Profile]:
        """Delete a profile."""
        # Use the service to delete the profile
        return self.profile_service.delete_profile(profile_id)
