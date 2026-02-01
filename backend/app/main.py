from fastapi import FastAPI
from app.config import setup_cors
from app.routes import resume, recommend, chat, generate
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="AIBIR Backend")

setup_cors(app)

app.include_router(resume.router)
app.include_router(recommend.router)
app.include_router(chat.router)
app.include_router(generate.router)

@app.get("/")
def root():
    return {"message": "AIBIR Backend is running 🚀"}

@app.on_event("startup")
async def startup_event():
    """Pre-warm the cache on startup for instant responses"""
    from app.services.web_scraper import scrape_all_jobs
    logger.info("⏳ Pre-warming job cache...")
    jobs = scrape_all_jobs()
    logger.info(f"✓ Cache ready with {len(jobs)} jobs")
