import pytest
from app.api.profile_api import ProfileApi
from app.db.profile_repository import ProfileRepository as ProfileRepositoryImpl
from app.db.profile_models import ProfileHistory
from app.entities import ProfileStatus
from app.api.profile_schemas import ProfileCreate, ProfileUpdate
from app.services.profile_service import ProfileService


def test_create_profile(db_session):
    """Test creating a profile using the ProfileApi."""
    # Create profile data with unique email
    import uuid

    unique_id = str(uuid.uuid4())
    profile_data = ProfileCreate(
        name="Test User",
        email=f"test_crud_{unique_id}@example.com",
        specialty="Testing",
        linkedin=f"https://linkedin.com/in/testcrud_{unique_id}",
    )

    # Create repository, service, and API
    repository = ProfileRepositoryImpl(db_session)
    service = ProfileService(repository)
    profile_service = ProfileApi(service)

    # Create profile
    profile = profile_service.create_profile(
        name=profile_data.name,
        email=profile_data.email,
        specialty=profile_data.specialty,
        linkedin=profile_data.linkedin
    )

    # Verify profile was created
    assert profile.id is not None
    assert profile.name == "Test User"
    assert profile.email == profile_data.email
    assert profile.specialty == "Testing"
    assert profile.linkedin == profile_data.linkedin
    assert profile.status == ProfileStatus.ACTIVE

    # Verify history was created
    histories = (
        db_session.query(ProfileHistory).filter(ProfileHistory.profile_id == profile.id).all()
    )
    assert len(histories) == 1
    assert histories[0].status == ProfileStatus.ACTIVE


def test_get_profile(db_session, test_profile):
    """Test getting a profile by ID."""
    # Create repository, service, and API
    repository = ProfileRepositoryImpl(db_session)
    service = ProfileService(repository)
    profile_service = ProfileApi(service)

    # Get the profile
    profile = profile_service.get_profile(test_profile.id)

    # Verify profile was retrieved
    assert profile is not None
    assert profile.id == test_profile.id
    assert profile.name == test_profile.name
    assert profile.email == test_profile.email


def test_get_profiles(db_session, test_profile):
    """Test getting multiple profiles with pagination."""
    # Create repository, service, and API
    repository = ProfileRepositoryImpl(db_session)
    service = ProfileService(repository)
    profile_service = ProfileApi(service)

    # Create another profile with unique email
    profile_data = ProfileCreate(
        name="Another User",
        email=f"another_{test_profile.id}@example.com",
        specialty="Another Specialty",
        linkedin="https://linkedin.com/in/anotheruser",
    )
    another_profile = profile_service.create_profile(
        name=profile_data.name,
        email=profile_data.email,
        specialty=profile_data.specialty,
        linkedin=profile_data.linkedin
    )

    # Get profiles with pagination
    profiles = profile_service.get_profiles(skip=0, limit=10)

    # Verify profiles were retrieved
    assert len(profiles) >= 2  # At least the test_profile and another_profile
    assert any(p.id == test_profile.id for p in profiles)
    assert any(p.id == another_profile.id for p in profiles)

    # Test pagination
    profiles_limited = profile_service.get_profiles(skip=0, limit=1)
    assert len(profiles_limited) == 1


def test_update_profile(db_session, test_profile):
    """Test updating a profile."""
    # Create repository, service, and API
    repository = ProfileRepositoryImpl(db_session)
    service = ProfileService(repository)
    profile_service = ProfileApi(service)

    # Update data
    update_data = ProfileUpdate(name="Updated Name", status="INACTIVE")

    # Update profile
    updated_profile = profile_service.update_profile(
        profile_id=test_profile.id,
        name=update_data.name,
        status=update_data.status
    )

    # Verify profile was updated
    assert updated_profile.name == "Updated Name"
    assert updated_profile.status == ProfileStatus.INACTIVE
    assert updated_profile.email == test_profile.email  # Unchanged

    # Verify history was created for status change
    histories = (
        db_session.query(ProfileHistory).filter(ProfileHistory.profile_id == test_profile.id).all()
    )
    assert len(histories) == 1
    assert histories[0].status == ProfileStatus.INACTIVE


def test_delete_profile(db_session, test_profile):
    """Test deleting a profile."""
    # Create repository, service, and API
    repository = ProfileRepositoryImpl(db_session)
    service = ProfileService(repository)
    profile_service = ProfileApi(service)

    # Store profile ID before deletion
    profile_id = test_profile.id

    # Delete profile
    deleted_profile = profile_service.delete_profile(profile_id)

    # Verify profile was deleted
    assert deleted_profile.id == profile_id

    # Verify profile no longer exists in database
    profile = profile_service.get_profile(profile_id)
    assert profile is None
