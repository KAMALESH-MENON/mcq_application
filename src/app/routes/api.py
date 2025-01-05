from fastapi import APIRouter

from app.routes.v1 import auth_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router.router)
