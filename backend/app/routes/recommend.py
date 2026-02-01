from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from app.services.data_store import get_student
from app.core.orchestrator import generate_recommendations
from app.services.web_scraper import scrape_all_jobs, search_jobs, get_jobs_by_source

router = APIRouter(prefix="/recommend")

@router.get("/{student_id}", response_model=Dict[str, Any])
def recommend(student_id: str):
    """Get recommendations with scraped jobs"""
    student = get_student(student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    recommendations = generate_recommendations(student["resume_text"])
    
    # Add scraped internships instead of LinkedIn URLs
    all_jobs = scrape_all_jobs()
    recommendations["internships"] = all_jobs
    recommendations["total_count"] = len(all_jobs)
    recommendations["sources"] = list(set(job["source"] for job in all_jobs))
    
    return recommendations


@router.get("/search/jobs", response_model=Dict[str, Any])
def search(q: str = Query(..., min_length=1), source: str = Query(None)):
    """Search jobs by title/company or filter by source"""
    
    if source:
        jobs = get_jobs_by_source(source)
    else:
        jobs = search_jobs(q)
    
    return {
        "query": q,
        "results": jobs,
        "count": len(jobs),
        "source_filter": source or "all"
    }


@router.get("/jobs/all", response_model=Dict[str, Any])
def get_all_jobs():
    """Get all scraped jobs with statistics"""
    jobs = scrape_all_jobs()
    
    # Group by source
    sources = {}
    for job in jobs:
        source = job["source"]
        if source not in sources:
            sources[source] = 0
        sources[source] += 1
    
    return {
        "total_jobs": len(jobs),
        "jobs": jobs,
        "by_source": sources,
        "last_updated": "Cached - refreshes hourly"
    }


@router.get("/jobs/source/{source_name}", response_model=Dict[str, Any])
def get_jobs_by_source_endpoint(source_name: str):
    """Get jobs from specific source"""
    jobs = get_jobs_by_source(source_name)
    
    return {
        "source": source_name,
        "count": len(jobs),
        "jobs": jobs
    }
