from fastapi import FastAPI, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.models.settlement import Settlement
from app.models.user_claim import UserClaim
from app.scrapers.kroll_scraper import SettlementScraper
from app.api.unclaimed_property import router as unclaimed_property_router
from app.api.perk_audit import router as perk_audit_router
from app.api.freebies import router as freebies_router
import asyncio

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Register API Routers
app.include_router(unclaimed_property_router, prefix=settings.API_V1_STR)
app.include_router(perk_audit_router, prefix=settings.API_V1_STR)
app.include_router(freebies_router, prefix=settings.API_V1_STR)

def run_scraper_task():
    scraper = SettlementScraper()
    asyncio.run(scraper.scrape_and_ingest())

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "docs": "/docs"
    }

@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {"status": "healthy"}

@app.get(f"{settings.API_V1_STR}/settlements")
def get_settlements(db: Session = Depends(get_db)):
    return db.query(Settlement).all()

@app.post(f"{settings.API_V1_STR}/scrapers/run")
def run_scraper(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scraper_task)
    return {"message": "Settlement scraper pipeline initiated in background!"}
