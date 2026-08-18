from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/unclaimed-property", tags=["Unclaimed Property"])

# Directory mapping for state treasury unclaimed property portals
STATE_PORTALS = {
    "PA": {
        "state_name": "Pennsylvania",
        "portal_name": "PA Treasury Unclaimed Property",
        "base_url": "https://unclaimedproperty.patreasury.gov",
        "search_url": "https://unclaimedproperty.patreasury.gov/en/Property/SearchIndex"
    },
    "NY": {
        "state_name": "New York",
        "portal_name": "NY Comptroller Unclaimed Funds",
        "base_url": "https://www.osc.ny.gov/unclaimed-funds",
        "search_url": "https://ouf.osc.state.ny.us/ouf/"
    },
    "CA": {
        "state_name": "California",
        "portal_name": "CA State Controller Unclaimed Property",
        "base_url": "https://claimit.ca.gov",
        "search_url": "https://claimit.ca.gov/en/Property/SearchIndex"
    },
    "TX": {
        "state_name": "Texas",
        "portal_name": "Texas Unclaimed Property (ClaimItTexas)",
        "base_url": "https://www.claimittexas.org",
        "search_url": "https://www.claimittexas.org/app/claim-search"
    },
    "FL": {
        "state_name": "Florida",
        "portal_name": "FL Division of Unclaimed Property",
        "base_url": "https://fltreasurehunt.gov",
        "search_url": "https://fltreasurehunt.gov/Control.do?_cmd=load-search"
    }
}

DEFAULT_NAUPA_URL = "https://www.missingmoney.com"

class SearchLinkResponse(BaseModel):
    state_code: str
    state_name: str
    portal_name: str
    direct_search_url: str
    requires_naupa_fallback: bool

@router.get("/states")
def get_supported_states():
    """Returns list of active direct-integration state portals."""
    return [
        {"code": code, "name": data["state_name"], "portal": data["portal_name"]}
        for code, data in STATE_PORTALS.items()
    ]

@router.get("/search-link", response_model=SearchLinkResponse)
def get_state_search_link(
    state_code: str = Query(..., description="Two-letter state postal abbreviation, e.g., PA, NY, CA"),
    first_name: Optional[str] = Query(None, description="User first name for pre-filling search"),
    last_name: Optional[str] = Query(None, description="User last name for pre-filling search")
):
    """Generates an optimized direct search link for a state treasury database."""
    code_upper = state_code.upper().strip()
    
    if code_upper in STATE_PORTALS:
        portal = STATE_PORTALS[code_upper]
        search_url = portal["search_url"]
        
        # Pre-fill query strings where state portals support URL parameters
        if last_name:
            if code_upper == "PA":
                search_url += f"?LastName={last_name}"
                if first_name:
                    search_url += f"&FirstName={first_name}"
        
        return SearchLinkResponse(
            state_code=code_upper,
            state_name=portal["state_name"],
            portal_name=portal["portal_name"],
            direct_search_url=search_url,
            requires_naupa_fallback=False
        )
    
    # Fallback to NAUPA / MissingMoney for states not yet mapped
    return SearchLinkResponse(
        state_code=code_upper,
        state_name=code_upper,
        portal_name="MissingMoney (NAUPA National Database)",
        direct_search_url=DEFAULT_NAUPA_URL,
        requires_naupa_fallback=True
    )
