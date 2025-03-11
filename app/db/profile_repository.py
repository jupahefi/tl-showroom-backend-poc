from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.entities import Profile, ProfileHistory, ProfileStatus
from app.db.profile_models import Profile as ProfileModel
from app.db.profile_models import ProfileHistory as ProfileHistoryModel
from app.db.profile_models import ProfileStatus as ProfileStatusModel


class ProfileRepository:
    """Repository for profile-related database operations."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_domain(self, model: ProfileModel) -> Profile:
        """Map a database model to a domain entity."""
        profile = Profile(
            id=model.id,
            name=model.name,
            email=model.email,
            specialty=model.specialty,
            linkedin=model.linkedin,
            status=ProfileStatus(model.status.value),
            start_date=model.start_date,
            end_date=model.end_date,
        )

        # Map history entries
        profile.history = [
            ProfileHistory(
                id=history.id,
                profile_id=history.profile_id,
                status=ProfileStatus(history.status.value),
                changed_at=history.changed_at,
                profile=profile,
            )
            for history in model.history
        ]

        return profile

    def _map_to_model(self, entity: Profile) -> ProfileModel:
        """Map a domain entity to a database model."""
        # If entity has an ID, it might already exist in the database
        if entity.id:
            model = self.db.query(ProfileModel).filter(ProfileModel.id == entity.id).first()
            if model:
                # Update existing model
                model.name = entity.name
                model.email = entity.email
                model.specialty = entity.specialty
                model.linkedin = entity.linkedin
                model.status = ProfileStatusModel(entity.status.value)
                model.start_date = entity.start_date
                model.end_date = entity.end_date
                return model

        # Create new model
        model = ProfileModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            specialty=entity.specialty,
            linkedin=entity.linkedin,
            status=ProfileStatusModel(entity.status.value),
            start_date=entity.start_date,
            end_date=entity.end_date,
        )

        return model

    def create(self, profile: Profile) -> Profile:
        """Create a new profile."""
        model = self._map_to_model(profile)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        # Set the ID from the database
        profile.id = model.id

        # Create history entry
        history_model = ProfileHistoryModel(
            profile_id=model.id, status=ProfileStatusModel(profile.status.value)
        )
        self.db.add(history_model)
        self.db.commit()

        return self._map_to_domain(model)

    def get_by_id(self, profile_id: int) -> Optional[Profile]:
        """Get a profile by ID."""
        model = self.db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not model:
            return None
        return self._map_to_domain(model)

    def get_all(self, skip: int = 0, limit: int = 10) -> List[Profile]:
        """Get all profiles with pagination."""
        models = self.db.query(ProfileModel).offset(skip).limit(limit).all()
        return [self._map_to_domain(model) for model in models]

    def update(self, profile: Profile) -> Profile:
        """Update a profile."""
        # Get the existing model
        model = self.db.query(ProfileModel).filter(ProfileModel.id == profile.id).first()
        if not model:
            return None

        # Update model fields
        model.name = profile.name
        model.email = profile.email
        model.specialty = profile.specialty
        model.linkedin = profile.linkedin
        model.status = ProfileStatusModel(profile.status.value)
        model.start_date = profile.start_date
        model.end_date = profile.end_date

        # Commit changes
        self.db.commit()
        self.db.refresh(model)

        # Create history entry for status changes
        # This matches the behavior in the original crud.py
        history_model = ProfileHistoryModel(
            profile_id=model.id, status=ProfileStatusModel(profile.status.value)
        )
        self.db.add(history_model)
        self.db.commit()
        self.db.refresh(model)

        return self._map_to_domain(model)

    def delete(self, profile_id: int) -> Optional[Profile]:
        """Delete a profile."""
        model = self.db.query(ProfileModel).filter(ProfileModel.id == profile_id).first()
        if not model:
            return None

        # Map to domain entity before deletion
        profile = self._map_to_domain(model)

        # Actually delete the profile from the database
        # This matches the behavior in the original crud.py
        self.db.delete(model)
        self.db.commit()

        return profile
