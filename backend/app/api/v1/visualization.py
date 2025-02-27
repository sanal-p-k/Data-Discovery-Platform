from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.visualization_service import VisualizationService  # Service layer for visualizations
from app.models.visualization import Visualization  # Visualization model (Pydantic or ORM)
from app.utils.auth import get_current_user  # Authentication dependency

# Create an APIRouter instance
router = APIRouter(prefix="/visualizations", tags=["visualizations"])

@router.post("/", response_model=Visualization)
async def create_visualization(
    dataset_id: int,
    chart_type: str,
    visualization_service: VisualizationService = Depends(VisualizationService),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a visualization (e.g., chart) for a specific dataset.
    """
    try:
        # Call the service layer to create a visualization
        visualization = visualization_service.create_visualization(dataset_id, chart_type)
        return visualization
    except Exception as e:
        # Handle errors and return appropriate HTTP status codes
        raise HTTPException(status_code=500, detail=str(e))