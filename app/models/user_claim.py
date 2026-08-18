from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class UserClaim(Base):
    __tablename__ = "user_claims"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(100), nullable=False, index=True, default="default-user")
    item_title = Column(String(255), nullable=False)
    item_type = Column(String(50), nullable=False) # SETTLEMENT, UNCLAIMED_PROPERTY, FREEBIE
    status = Column(String(30), nullable=False, default="SAVED") # SAVED, SUBMITTED, PAID
    estimated_payout = Column(Numeric(10, 2), nullable=True)
    payout_received = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
