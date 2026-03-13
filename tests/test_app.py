import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Test client fixture for FastAPI app"""
    return TestClient(app)

def test_get_activities(client):
    """Test GET /activities endpoint returns all activities"""
    # Arrange - no setup needed

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" == data["message"]

    # Verify email was added to participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]

def test_signup_duplicate(client):
    """Test signup fails when student is already signed up"""
    # Arrange
    activity_name = "Programming Class"
    email = "duplicate@example.com"
    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act - try to signup again
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is already signed up for this activity" == data["detail"]

def test_signup_activity_not_found(client):
    """Test signup fails for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]

def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Gym Class"
    email = "unregister@example.com"
    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Unregistered {email} from {activity_name}" == data["message"]

    # Verify email was removed from participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]

def test_unregister_not_signed_up(client):
    """Test unregister fails when student is not signed up"""
    # Arrange
    activity_name = "Soccer Team"
    email = "notsignedup@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student is not signed up for this activity" == data["detail"]

def test_unregister_activity_not_found(client):
    """Test unregister fails for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "test@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" == data["detail"]