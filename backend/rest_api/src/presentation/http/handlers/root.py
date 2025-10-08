from fastapi import APIRouter

from src.presentation.http.handlers.auth import router as auth_router
from src.presentation.http.handlers.profiles import router as profiles_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(profiles_router)