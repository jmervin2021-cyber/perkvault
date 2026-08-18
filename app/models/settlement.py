from sqlalchemy import Column, String, Text, Numeric, DateTime, Boolean
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default="CONSUMER")
    proof_type = Column(String(30), nullable=False, default="NO_PROOF") # NO_PROOF, PROOF_REQUIRED
    estimated_payout_min = Column(Numeric(10, 2), nullable=True)
    estimated_payout_max = Column(Numeric(10, 2), nullable=True)
    claim_deadline = Column(DateTime(timezone=True), nullable=True)
    official_claim_url = Column(Text, nullable=False)
    administrator_name = Column(String(100), nullable=True)
    is_verified = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
