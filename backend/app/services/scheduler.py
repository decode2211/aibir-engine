"""
Background scheduler for periodic web scraping
Refreshes job cache every hour
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.services.web_scraper import scrape_all_jobs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def schedule_scraper():
    """Start background scraper scheduler"""
    if not scheduler.running:
        # Scrape every hour
        scheduler.add_job(
            scrape_all_jobs,
            IntervalTrigger(hours=1),
            id='job_scraper',
            name='Hourly job scraper',
            replace_existing=True
        )
        scheduler.start()
        logger.info("✓ Job scraper scheduler started (hourly refresh)")


def stop_scraper():
    """Stop the scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("✓ Job scraper scheduler stopped")


def get_scheduler():
    """Get scheduler instance"""
    return scheduler
