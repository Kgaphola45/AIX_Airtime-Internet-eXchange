from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    description: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class WalletBase(BaseModel):
    balance: float

class WalletResponse(WalletBase):
    id: int
    user_id: int
    transactions: List[TransactionResponse] = []

    class Config:
        from_attributes = True

class WalletLoad(BaseModel):
    amount: float
