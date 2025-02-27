from pydantic import BaseModel
from typing import Optional

class VisualizationBase(BaseModel):
    dataset_id: int
    chart_type: str

class VisualizationCreate(VisualizationBase):
    pass

class Visualization(VisualizationBase):
    id: int
    created_at: str  # Use datetime if needed

    class Config:
        orm_mode = True  # Enable ORM compatibility