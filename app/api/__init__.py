from fastapi import APIRouter
from .public import router as public


router = APIRouter(prefix="/api/v1")
router.include_router(public)
