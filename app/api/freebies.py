from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/freebies", tags=["Daily Freebies & Rebates"])

FREEBIES_CATALOG = [
    {
        "id": "far-organic-snack",
        "title": "100% Free Organic Energy Bar",
        "type": "FREE_AFTER_REBATE",
        "value": 3.49,
        "merchant": "Target / Whole Foods",
        "rebate_method": "Venmo / PayPal via Aisle SMS",
        "instructions": "Buy product at retail, text photo of receipt, get 100% cash back in 24 hours."
    },
    {
        "id": "far-sparkling-water",
        "title": "100% Cash-Back Sparkling Water Can",
        "type": "FREE_AFTER_REBATE",
        "value": 2.99,
        "merchant": "Walmart / Kroger",
        "rebate_method": "Direct PayPal Deposit",
        "instructions": "Submit receipt upload to receive full purchase price reimbursement."
    },
    {
        "id": "bday-starbucks",
        "title": "Free Birthday Beverage or Food Item",
        "type": "BIRTHDAY_REWARD",
        "value": 6.50,
        "merchant": "Starbucks",
        "rebate_method": "In-App Reward Card",
        "instructions": "Join Starbucks Rewards at least 7 days before your birthday to unlock a free drink."
    },
    {
        "id": "bday-sephora",
        "title": "Free Birthday Gift Set",
        "type": "BIRTHDAY_REWARD",
        "value": 15.00,
        "merchant": "Sephora",
        "rebate_method": "Beauty Insider Account",
        "instructions": "Claim during your birthday month in-store or online with zero purchase minimum."
    }
]

@router.get("/catalog")
def get_freebies_catalog(
    category: Optional[str] = Query(None, description="Filter by type: FREE_AFTER_REBATE or BIRTHDAY_REWARD")
):
    """Returns active 100% free consumer product rebates and birthday freebie offers."""
    if category:
        filtered = [item for item in FREEBIES_CATALOG if item["type"] == category.upper()]
        return {"count": len(filtered), "items": filtered}
    
    return {"count": len(FREEBIES_CATALOG), "items": FREEBIES_CATALOG}
