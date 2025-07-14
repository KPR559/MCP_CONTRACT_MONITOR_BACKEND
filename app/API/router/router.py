from fastapi import APIRouter
from ..endpoints import ws, update

router = APIRouter(prefix="/api", tags=["api"])

# Include all routers
router.include_router(ws.router)
router.include_router(update.router)
