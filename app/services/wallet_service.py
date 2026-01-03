from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.models.transaction import Transaction

def get_wallet(db: Session, user_id: int):
    return db.query(Wallet).filter(Wallet.user_id == user_id).first()

def load_wallet(db: Session, user_id: int, amount: float):
    wallet = get_wallet(db, user_id)
    if not wallet:
        return None
    
    wallet.balance += amount
    
    # Log transaction
    transaction = Transaction(
        user_id=user_id,
        type="credit",
        amount=amount,
        description="Airtime load"
    )
    db.add(transaction)
    db.commit()
    db.refresh(wallet)
    return wallet
