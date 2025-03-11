from datetime import datetime
from typing import Optional, List
from app.entities import Profile, ProfileHistory, ProfileStatus


class ProfileService:
    """Domain service for profile-related business logic."""

    def __init__(self, profile_repository):
        self.profile_repository = profile_repository

    def create_profile(
        self, name: str, email: str, specialty: str, linkedin: Optional[str] = None
    ) -> Profile:
        """Create a new profile with initial status."""
        profile = Profile(
            name=name,
            email=email,
            specialty=specialty,
            linkedin=linkedin,
            status=ProfileStatus.ACTIVE,
            start_date=datetime.utcnow(),
        )

        # Create initial history entry
        history = ProfileHistory(
            profile_id=profile.id,
            status=profile.status,
            changed_at=datetime.utcnow(),
            profile=profile,
        )

        profile.history.append(history)

        # Persist to database using repository
        return self.profile_repository.create(profile)

    def update_profile(
        self,
        profile: Profile,
        name: Optional[str] = None,
        email: Optional[str] = None,
        specialty: Optional[str] = None,
        linkedin: Optional[str] = None,
        status: Optional[ProfileStatus] = None,
    ) -> Profile:
        """Update a profile and record status changes."""
        if name is not None:
            profile.name = name
        if email is not None:
            profile.email = email
        if specialty is not None:
            profile.specialty = specialty
        if linkedin is not None:
            profile.linkedin = linkedin

        # If status changed, record it in history
        if status is not None and profile.status != status:
            profile.status = status
            history = ProfileHistory(
                profile_id=profile.id, status=status, changed_at=datetime.utcnow(), profile=profile
            )
            profile.history.append(history)

        # Persist changes to database using repository
        return self.profile_repository.update(profile)

    def delete_profile(self, profile_id: int) -> Optional[Profile]:
        """Mark a profile as deleted."""
        profile = self.profile_repository.get_by_id(profile_id)
        if not profile:
            return None

        profile.status = ProfileStatus.DELETED
        profile.end_date = datetime.utcnow()

        # Record the deletion in history
        history = ProfileHistory(
            profile_id=profile.id,
            status=ProfileStatus.DELETED,
            changed_at=datetime.utcnow(),
            profile=profile,
        )
        profile.history.append(history)

        # Use repository to delete the profile
        return self.profile_repository.delete(profile_id)

    def get_profile(self, profile_id: int) -> Optional[Profile]:
        """Get a profile by ID."""
        return self.profile_repository.get_by_id(profile_id)

    def get_profiles(self, skip: int = 0, limit: int = 10) -> List[Profile]:
        """Get all profiles with pagination."""
        return self.profile_repository.get_all(skip, limit)