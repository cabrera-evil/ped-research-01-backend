"""API v1 router aggregation."""

from fastapi import APIRouter, Depends

from app.core.security import verify_api_key
from app.modules.inventory.routes import public_router as inventory_router
from app.modules.system.routes import protected_router, public_router

router = APIRouter()
router.include_router(public_router)
router.include_router(protected_router, dependencies=[Depends(verify_api_key)])
router.include_router(inventory_router, prefix="/inventory")
