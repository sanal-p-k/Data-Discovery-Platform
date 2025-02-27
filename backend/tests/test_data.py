from fastapi import status
from app.models.dataset import Dataset

def test_query_datasets(client):
    # Add test data to the database
    dataset = Dataset(id=1, name="Sales Data", description="Monthly sales data", created_at="2023-10-01", updated_at="2023-10-01")
    db = client.app.dependency_overrides[get_db]().__next__()
    db.add(dataset)
    db.commit()

    # Test the endpoint
    response = client.get("/datasets", params={"filter": "Sales", "limit": 1})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Sales Data"