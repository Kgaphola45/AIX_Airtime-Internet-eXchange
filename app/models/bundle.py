from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base

class Bundle(Base):
    __tablename__ = "bundles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String) # data, voice, sms
    amount = Column(Float)
    expiry = Column(DateTime)

    owner = relationship("User", back_populates="bundles")
