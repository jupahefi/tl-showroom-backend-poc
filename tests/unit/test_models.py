import pytest
from datetime import datetime
from app.db.profile_models import Profile, ProfileHistory
from app.entities import ProfileStatus


def test_profile_model(db_session):
    """Test creating a Profile model instance."""
    # Create a new profile
    profile = Profile(
        name="John Doe",
        email="john@example.com",
        specialty="Software Engineering",
        linkedin="https://linkedin.com/in/johndoe",
        status=ProfileStatus.ACTIVE,
    )

    # Add to session and commit
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    # Verify the profile was created with correct attributes
    assert profile.id is not None
    assert profile.name == "John Doe"
    assert profile.email == "john@example.com"
    assert profile.specialty == "Software Engineering"
    assert profile.linkedin == "https://linkedin.com/in/johndoe"
    assert profile.status == ProfileStatus.ACTIVE
    assert isinstance(profile.start_date, datetime)
    assert profile.end_date is None


def test_profile_history_model(db_session):
    """Test creating a ProfileHistory model instance."""
    # Create a profile first
    profile = Profile(
        name="Jane Smith",
        email="jane@example.com",
        specialty="Data Science",
        status=ProfileStatus.ACTIVE,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    # Create a history entry
    history = ProfileHistory(profile_id=profile.id, status=ProfileStatus.ACTIVE)
    db_session.add(history)
    db_session.commit()
    db_session.refresh(history)

    # Verify the history entry was created with correct attributes
    assert history.id is not None
    assert history.profile_id == profile.id
    assert history.status == ProfileStatus.ACTIVE
    assert isinstance(history.changed_at, datetime)

    # Verify the relationship works
    assert history.profile.id == profile.id
    assert profile.history[0].id == history.id


def test_profile_status_enum():
    """Test the ProfileStatus enum values."""
    assert ProfileStatus.ACTIVE.value == "active"
    assert ProfileStatus.INACTIVE.value == "inactive"
    assert ProfileStatus.SUSPENDED.value == "suspended"
    assert ProfileStatus.DELETED.value == "deleted"
