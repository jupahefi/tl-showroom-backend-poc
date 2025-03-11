import pytest
from fastapi.testclient import TestClient
from app.entities import ProfileStatus


def test_create_profile(client):
    """Test creating a profile via the API."""
    # Profile data with unique email
    import uuid

    unique_id = str(uuid.uuid4())
    profile_data = {
        "name": "API Test User",
        "email": f"api_test_{unique_id}@example.com",
        "specialty": "API Testing",
        "linkedin": f"https://linkedin.com/in/apitester_{unique_id}",
    }

    # Send POST request
    response = client.post("/profiles/", json=profile_data)

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == profile_data["name"]
    assert data["email"] == profile_data["email"]
    assert data["specialty"] == profile_data["specialty"]
    assert data["linkedin"] == profile_data["linkedin"]
    assert data["status"] == ProfileStatus.ACTIVE.value
    assert "id" in data
    assert "start_date" in data


def test_get_profile(client, test_profile):
    """Test getting a profile by ID via the API."""
    # Send GET request
    response = client.get(f"/profiles/{test_profile.id}")

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_profile.id
    assert data["name"] == test_profile.name
    assert data["email"] == test_profile.email
    assert data["specialty"] == test_profile.specialty


def test_get_profile_not_found(client):
    """Test getting a non-existent profile via the API."""
    # Send GET request for non-existent profile
    response = client.get("/profiles/9999")

    # Verify response
    assert response.status_code == 404
    assert "detail" in response.json()


def test_get_profiles(client, test_profile):
    """Test getting all profiles via the API."""
    # Create another profile first with unique email
    profile_data = {
        "name": "Another API User",
        "email": f"another_api_{test_profile.id}@example.com",
        "specialty": "Another API Testing",
    }
    client.post("/profiles/", json=profile_data)

    # Send GET request
    response = client.get("/profiles/")

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # At least the test_profile and the one we just created

    # Test pagination
    response = client.get("/profiles/?skip=0&limit=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_update_profile(client, test_profile):
    """Test updating a profile via the API."""
    # Update data
    update_data = {"name": "Updated API Name", "status": "INACTIVE"}

    # Send PUT request
    response = client.put(f"/profiles/{test_profile.id}", json=update_data)

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["status"] == ProfileStatus.INACTIVE.value
    assert data["email"] == test_profile.email  # Unchanged


def test_update_profile_not_found(client):
    """Test updating a non-existent profile via the API."""
    # Send PUT request for non-existent profile
    response = client.put("/profiles/9999", json={"name": "Not Found"})

    # Verify response
    assert response.status_code == 404
    assert "detail" in response.json()


def test_delete_profile(client, test_profile):
    """Test deleting a profile via the API."""
    # Send DELETE request
    response = client.delete(f"/profiles/{test_profile.id}")

    # Verify response
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Perfil eliminado"

    # Verify profile is deleted
    response = client.get(f"/profiles/{test_profile.id}")
    assert response.status_code == 404


def test_delete_profile_not_found(client):
    """Test deleting a non-existent profile via the API."""
    # Send DELETE request for non-existent profile
    response = client.delete("/profiles/9999")

    # Verify response
    assert response.status_code == 404
    assert "detail" in response.json()


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
