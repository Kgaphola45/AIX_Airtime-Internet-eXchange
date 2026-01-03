from fastapi import APIRouter
from app.api.v1 import auth, wallet, bundle, usage

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(bundle.router, prefix="/bundles", tags=["bundles"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
