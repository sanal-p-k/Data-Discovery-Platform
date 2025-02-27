from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import Base, engine, get_db
from models.dataset import Dataset
from models.user import User
from models.visualization import Visualization
from services.data_service import DataService
from services.visualization_service import VisualizationService
from services.user_service import UserService
from utils.auth import get_current_user

# Create the database tables (for development only)
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI()

# Dependency for services
def get_data_service(db: Session = Depends(get_db)):
    return DataService(db)

def get_visualization_service(db: Session = Depends(get_db)):
    return VisualizationService(db)

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

# Example endpoints
@app.get("/datasets", response_model=list[Dataset])
async def get_datasets(
    filter: str = None,
    limit: int = 10,
    data_service: DataService = Depends(get_data_service),
):
    """
    Query datasets with optional filters and limits.
    """
    datasets = data_service.query_datasets(filter=filter, limit=limit)
    return datasets

@app.post("/visualizations", response_model=Visualization)
async def create_visualization(
    dataset_id: int,
    chart_type: str,
    visualization_service: VisualizationService = Depends(get_visualization_service),
):
    """
    Create a visualization for a dataset.
    """
    visualization = visualization_service.create_visualization(dataset_id, chart_type)
    return visualization

@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's details.
    """
    return current_user