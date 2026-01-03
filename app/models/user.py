from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    wallet = relationship("Wallet", back_populates="owner", uselist=False)
    bundles = relationship("Bundle", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")
