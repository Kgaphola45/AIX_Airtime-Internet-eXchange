from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BundleBase(BaseModel):
    type: str
    amount: float

class BundlePurchase(BundleBase):
    pass

class BundleResponse(BundleBase):
    id: int
    user_id: int
    expiry: datetime

    class Config:
        from_attributes = True
