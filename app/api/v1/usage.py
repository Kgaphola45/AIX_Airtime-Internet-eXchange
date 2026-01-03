from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.services.usage_service import simulate_usage

router = APIRouter()

class UsageRequest(BaseModel):
    type: str # data, voice, sms
    amount: float

@router.post("/simulate")
def usage_simulation(usage: UsageRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    success = simulate_usage(db, current_user.id, usage.type, usage.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Insufficient bundle balance")
    return {"message": "Usage simulated successfully", "deducted": usage.amount}
