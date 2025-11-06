from fastapi import APIRouter

from src.presentation.http.handlers.auth import router as auth_router
from src.presentation.http.handlers.profiles import router as profiles_router
from src.presentation.http.handlers.wallets import router as wallet_router
from src.presentation.http.handlers.transactions import router as transactions_router
from src.presentation.http.handlers.products import router as products_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(profiles_router)
router.include_router(wallet_router)
router.include_router(transactions_router)
router.include_router(products_router)
