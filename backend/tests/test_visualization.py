from fastapi import status
from app.models.visualization import Visualization
from backend.app.db import get_db
from backend.app.models.dataset import Dataset

def test_create_visualization(client):
    # Add test data to the database
    dataset = Dataset(id=1, name="Sales Data", description="Monthly sales data", created_at="2023-10-01", updated_at="2023-10-01")
    db = client.app.dependency_overrides[get_db]().__next__()
    db.add(dataset)
    db.commit()

    # Test the endpoint
    response = client.post(
        "/visualizations",
        json={"dataset_id": 1, "chart_type": "bar"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["dataset_id"] == 1
    assert response.json()["chart_type"] == "bar"