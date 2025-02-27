from fastapi import APIRouter
from .data import router as data_router
from .visualizations import router as visualizations_router
from .auth import router as auth_router

# Create a parent APIRouter for v1
router = APIRouter(prefix="/v1")

# Include all routers
router.include_router(data_router)
router.include_router(visualizations_router)
router.include_router(auth_router)