from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.bundle import BundleResponse, BundlePurchase
from app.services.bundle_service import buy_bundle

router = APIRouter()

@router.post("/buy", response_model=BundleResponse)
def purchase_bundle(purchase: BundlePurchase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Simple logic for expiry: 30 days from now
    expiry = datetime.utcnow() + timedelta(days=30)
    # Using amount as cost for simplicity in this MVP
    bundle = buy_bundle(db, current_user.id, purchase.type, purchase.amount, purchase.amount, expiry)
    if not bundle:
        raise HTTPException(status_code=400, detail="Insufficient funds or invalid wallet")
    return bundle

@router.get("/my-bundles", response_model=List[BundleResponse])
def read_my_bundles(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.bundles
