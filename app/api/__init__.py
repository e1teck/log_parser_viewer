from fastapi import APIRouter
from .public import router as public


router = APIRouter()
router.include_router(public)
