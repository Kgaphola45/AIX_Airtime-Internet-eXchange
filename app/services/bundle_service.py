from datetime import datetime
from sqlalchemy.orm import Session
from app.models.bundle import Bundle
from app.models.transaction import Transaction
from app.services.wallet_service import get_wallet

def buy_bundle(db: Session, user_id: int, bundle_type: str, amount: float, cost: float, expiry: datetime):
    wallet = get_wallet(db, user_id)
    if not wallet or wallet.balance < cost:
        return None
    
    # Deduct from wallet
    wallet.balance -= cost
    
    # Create Bundle
    bundle = Bundle(
        user_id=user_id,
        type=bundle_type,
        amount=amount,
        expiry=expiry
    )
    db.add(bundle)
    
    # Log Transaction
    transaction = Transaction(
        user_id=user_id,
        type="debit",
        amount=cost,
        description=f"Purchase {bundle_type} bundle of {amount}"
    )
    db.add(transaction)
    
    db.commit()
    return bundle
