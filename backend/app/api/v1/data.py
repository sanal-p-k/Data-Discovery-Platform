from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.services.data_service import DataService  # Service layer for business logic
from app.models.dataset import Dataset  # Dataset model (Pydantic or ORM)
from app.utils.auth import get_current_user  # Authentication dependency

# Create an APIRouter instance
router = APIRouter(prefix="/data", tags=["data"])

@router.get("/", response_model=List[Dataset])
async def query_datasets(
    filter: Optional[str] = Query(None, description="Filter datasets by a keyword"),
    limit: Optional[int] = Query(10, description="Limit the number of results"),
    data_service: DataService = Depends(DataService),
    current_user: dict = Depends(get_current_user),
):
    """
    Query datasets with optional filters and limits.
    Returns a list of datasets.
    """
    try:
        # Call the service layer to fetch datasets
        datasets = data_service.query_datasets(filter=filter, limit=limit)
        return datasets
    except Exception as e:
        # Handle errors and return appropriate HTTP status codes
        raise HTTPException(status_code=500, detail=str(e))