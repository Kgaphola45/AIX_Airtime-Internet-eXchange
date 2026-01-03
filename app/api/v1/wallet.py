from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.wallet import WalletResponse, WalletLoad
from app.services.wallet_service import get_wallet, load_wallet

router = APIRouter()

@router.get("/balance", response_model=WalletResponse)
def get_balance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = get_wallet(db, current_user.id)
    if not wallet:
        # Should ideally be created on registration, but for safety
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/load", response_model=WalletResponse)
def load_airtime(load_in: WalletLoad, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = load_wallet(db, current_user.id, load_in.amount)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
