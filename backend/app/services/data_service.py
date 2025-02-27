from typing import List, Optional
from models.dataset import Dataset

class DataService:
    def __init__(self):
        # Mock data for demonstration
        self.datasets = [
            Dataset(id=1, name="Sales Data", description="Monthly sales data", created_at="2023-10-01", updated_at="2023-10-01"),
            Dataset(id=2, name="Customer Data", description="Customer demographics", created_at="2023-10-02", updated_at="2023-10-02"),
            Dataset(id=3, name="Inventory Data", description="Product inventory levels", created_at="2023-10-03", updated_at="2023-10-03"),
        ]

    def query_datasets(self, filter: Optional[str] = None, limit: Optional[int] = 10) -> List[Dataset]:
        """
        Query datasets with optional filters and limits.
        """
        # Apply filter if provided
        if filter:
            filtered_datasets = [dataset for dataset in self.datasets if filter.lower() in dataset.name.lower()]
        else:
            filtered_datasets = self.datasets

        # Apply limit
        return filtered_datasets[:limit]