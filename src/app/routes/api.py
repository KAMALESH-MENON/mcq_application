from fastapi import APIRouter

from app.routes.v1 import admin_routers, auth_router, mcq_routes

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router.router)
router.include_router(mcq_routes.router)
router.include_router(admin_routers.router)
