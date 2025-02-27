from fastapi import status
from app.models.user import User
from backend.app.db import get_db

def test_login_for_access_token(client):
    # Add test user to the database
    user = User(id=1, username="admin", email="admin@example.com", disabled=False)
    db = client.app.dependency_overrides[get_db]().__next__()
    db.add(user)
    db.commit()

    # Test the endpoint
    response = client.post(
        "/token",
        data={"username": "admin", "password": "password"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_read_users_me(client):
    # Add test user to the database
    user = User(id=1, username="admin", email="admin@example.com", disabled=False)
    db = client.app.dependency_overrides[get_db]().__next__()
    db.add(user)
    db.commit()

    # Get an access token
    token_response = client.post(
        "/token",
        data={"username": "admin", "password": "password"},
    )
    token = token_response.json()["access_token"]

    # Test the endpoint
    response = client.get(
        "/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "admin"