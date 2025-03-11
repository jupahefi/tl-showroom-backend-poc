import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from app.config.database import Base, get_db
from app.main import app
from app.db.profile_models import Profile
from app.entities import ProfileStatus

# Test database URL - using SQLite in-memory database for tests
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def test_engine():
    """Create a SQLite in-memory database engine for testing."""
    # Remove existing test database if it exists
    if os.path.exists("./test.db"):
        os.remove("./test.db")

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield engine

    # Clean up after tests
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Create a new database session for a test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client for the FastAPI app."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    # Remove the override after the test
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_profile(db_session, request):
    """Create a test profile for testing."""
    # Generate unique email and linkedin for each test function
    import uuid

    unique_id = str(uuid.uuid4())
    test_name = request.node.name
    profile = Profile(
        name="Test User",
        email=f"test_{test_name}_{unique_id}@example.com",
        specialty="Testing",
        linkedin=f"https://linkedin.com/in/testuser_{test_name}_{unique_id}",
        status=ProfileStatus.ACTIVE,
    )
    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)
    return profile
