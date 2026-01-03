from sqlalchemy.orm import Session
from app.models.bundle import Bundle

def simulate_usage(db: Session, user_id: int, usage_type: str, amount: float):
    # Find valid bundle
    bundle = db.query(Bundle).filter(
        Bundle.user_id == user_id, 
        Bundle.type == usage_type,
        Bundle.amount >= amount
    ).first()
    
    if bundle:
        bundle.amount -= amount
        db.commit()
        return True
    return False
