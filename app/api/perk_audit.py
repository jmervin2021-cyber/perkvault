from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/perk-audit", tags=["Perk & Digital Audit"])

# Carrier Perks Data Store
CARRIER_PERKS = {
    "VERIZON": [
        {"title": "Disney+ Premium Bundle", "value_monthly": 19.99, "eligible_plans": ["Unlimited Plus", "Unlimited Ultimate"], "action_guide": "Enroll via myVerizon App -> Account -> Services & Perks."},
        {"title": "Netflix & Max Bundle", "value_monthly": 10.00, "eligible_plans": ["myPlan Add-on"], "action_guide": "Activate $10/mo perk savings through myVerizon dashboard."},
        {"title": "Apple One / Apple Music", "value_monthly": 10.99, "eligible_plans": ["5G Get More", "5G Play More"], "action_guide": "Manage Add-ons in myVerizon to link Apple ID."}
    ],
    "TMOBILE": [
        {"title": "Netflix on Us", "value_monthly": 15.49, "eligible_plans": ["Go5G Plus", "Go5G Next", "Magenta MAX"], "action_guide": "Log into T-Mobile account -> Account Services -> Manage Add-ons."},
        {"title": "Hulu (With Ads)", "value_monthly": 7.99, "eligible_plans": ["Go5G Next"], "action_guide": "Redeem through T-Mobile Account Promotions page."},
        {"title": "Apple TV+", "value_monthly": 9.99, "eligible_plans": ["Go5G Plus", "Go5G Next"], "action_guide": "Claim pass via T-Life / T-Mobile Tuesdays app."}
    ],
    "ATT": [
        {"title": "Max (HBO) Included", "value_monthly": 15.99, "eligible_plans": ["Unlimited Elite (Legacy)"], "action_guide": "Log into Max app using AT&T provider credentials."},
        {"title": "ActiveArmor Advanced Security", "value_monthly": 3.99, "eligible_plans": ["Unlimited Extra EL", "Unlimited Premium PL"], "action_guide": "Download AT&T ActiveArmor app and sign in."}
    ]
}

# Library Digital Perks Catalog
LIBRARY_PERKS = [
    {"name": "Kanopy", "type": "Streaming Video", "estimated_annual_value": 120.00, "description": "Free access to thousands of movies, documentaries, and indie films using your library card."},
    {"name": "Hoopla Digital", "type": "Audiobooks & eBooks", "estimated_annual_value": 180.00, "description": "Instant download of audiobooks, comics, music, and movies with zero hold queues."},
    {"name": "LinkedIn Learning", "type": "Professional Skills", "estimated_annual_value": 360.00, "description": "Full access to 16,000+ expert-led courses and professional certifications."},
    {"name": "PressReader / NYT", "type": "Newspapers & Journalism", "estimated_annual_value": 200.00, "description": "Free digital access to major national newspapers and global magazines."}
]

class PerkItem(BaseModel):
    title: str
    value_monthly: float
    eligible_plans: List[str]
    action_guide: str

class AuditResponse(BaseModel):
    carrier: str
    unlocked_monthly_value: float
    unlocked_annual_value: float
    available_perks: List[PerkItem]

@router.get("/carrier-audit", response_model=AuditResponse)
def audit_carrier_perks(
    carrier: str = Query(..., description="Carrier name: VERIZON, TMOBILE, or ATT")
):
    """Audits cell phone plan provider to reveal hidden free streaming and digital perks."""
    carrier_key = carrier.upper().strip()
    perks_found = CARRIER_PERKS.get(carrier_key, [])
    
    total_monthly = sum(item["value_monthly"] for item in perks_found)
    
    return AuditResponse(
        carrier=carrier_key,
        unlocked_monthly_value=total_monthly,
        unlocked_annual_value=total_monthly * 12,
        available_perks=perks_found
    )

@router.get("/library-vault")
def get_library_perks():
    """Returns the free digital subscription catalog available through local public library cards."""
    total_annual_value = sum(item["estimated_annual_value"] for item in LIBRARY_PERKS)
    return {
        "total_annual_value": total_annual_value,
        "perks": LIBRARY_PERKS,
        "action_required": "Get a free library card from your local county public library system."
    }
