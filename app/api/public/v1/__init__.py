from fastapi import APIRouter

from .log_messages import router as log_messages_router


router = APIRouter(prefix="/v1")
router.include_router(log_messages_router)