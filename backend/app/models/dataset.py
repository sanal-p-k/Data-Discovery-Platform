from pydantic import BaseModel
from typing import Optional

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int
    created_at: str  # Use datetime if needed
    updated_at: str  # Use datetime if needed

    class Config:
        orm_mode = True  # Enable ORM compatibility