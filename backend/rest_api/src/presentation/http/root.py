from fastapi import APIRouter

from src.presentation.http.auth import router as auth_router

router = APIRouter()

router.include_router(auth_router)