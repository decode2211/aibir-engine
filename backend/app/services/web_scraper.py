"""
REAL-TIME WEB SCRAPER - Using SerpAPI for Live Job Listings
===========================================================
Fetches live job listings from Google Jobs, Indeed, Naukri, Internshala via SerpAPI.
"""

import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache with 15-minute TTL for live data
JOB_CACHE = {"data": [], "timestamp": None, "expires_in": 900}

DEFAULT_QUERY = "software internship"
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "a4a2744c06fad4efd58020dbc03015245905cc146b18bef37abb6e1e0199dc7b")
SERPAPI_BASE = "https://serpapi.com/search"


def _safe_get(url: str, params: dict = None) -> Optional[dict]:
    """Safely fetch JSON from SerpAPI."""
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code != 200:
            logger.warning(f"HTTP {response.status_code} for {url} - {response.text[:200]}")
            return None
        return response.json()
    except Exception as e:
        logger.warning(f"Request failed for {url}: {e}")
        return None


def _normalize_job(
    *,
    title: str,
    company: str,
    location: str,
    link: str,
    source: str,
    description: str = "",
    salary: str = "Not specified",
) -> Dict:
    """Normalize job data to standard format."""
    return {
        "title": title.strip() if title else "",
        "company": company.strip() if company else "",
        "location": location.strip() if location else "India",
        "salary": salary.strip() if salary else "Not specified",
        "description": description.strip() if description else "",
        "link": link,
        "deadline": (datetime.now() + timedelta(days=30)).isoformat(),
        "source": source,
        "skills": [],
    }


def _build_query(resume_text: Optional[str]) -> str:
    """Build search query from resume if provided."""
    if not resume_text:
        return DEFAULT_QUERY
    resume_lower = resume_text.lower()
    TECH_SKILLS = [
        "python", "java", "javascript", "react", "nodejs", "fastapi", "django",
        "sql", "mongodb", "aws", "docker", "kubernetes", "git", "linux", "kotlin",
    ]
    matched = [s for s in TECH_SKILLS if s in resume_lower]
    if matched:
        return f"{matched[0]} internship"
    return DEFAULT_QUERY


def fetch_google_jobs(query: str) -> List[Dict]:
    """Fetch jobs from Google Jobs via SerpAPI (covers Indeed, LinkedIn, etc)."""
    jobs: List[Dict] = []
    try:
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": "India",
            "api_key": SERPAPI_KEY,
        }
        data = _safe_get(SERPAPI_BASE, params)
        if not data:
            logger.warning(f"No response from SerpAPI for query: {query}")
            return jobs
        
        if "jobs_results" not in data:
            logger.warning(f"No 'jobs_results' in response. Keys: {list(data.keys())}")
            return jobs
        
        for job in data.get("jobs_results", [])[:15]:
            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("location", "")
            link = job.get("share_link", "") or job.get("link", "")  # Use share_link if available
            description = job.get("description", "")
            salary = job.get("salary", "") or job.get("detected_extensions", {}).get("salary", "Not specified")
            
            if title and company and link:
                jobs.append(
                    _normalize_job(
                        title=title,
                        company=company,
                        location=location,
                        link=link,
                        source="Google Jobs",
                        description=description,
                        salary=salary,
                    )
                )
        
        logger.info(f"✓ Google Jobs: {len(jobs)} live jobs fetched from {len(data.get('jobs_results', []))} total results")
    except Exception as e:
        logger.error(f"Google Jobs error: {e}", exc_info=True)
    return jobs


def fetch_indeed_direct(query: str) -> List[Dict]:
    """Indeed via google_jobs (since 'indeed' engine not available)."""
    jobs: List[Dict] = []
    try:
        params = {
            "engine": "google_jobs",
            "q": f"{query} site:indeed.com",
            "location": "India",
            "api_key": SERPAPI_KEY,
        }
        data = _safe_get(SERPAPI_BASE, params)
        if not data or "jobs_results" not in data:
            return jobs
        
        for job in data.get("jobs_results", [])[:10]:
            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("location", "")
            link = job.get("share_link", "") or job.get("link", "")
            salary = job.get("salary", "") or job.get("detected_extensions", {}).get("salary", "Not specified")
            
            if title and company and link:
                jobs.append(
                    _normalize_job(
                        title=title,
                        company=company,
                        location=location,
                        link=link,
                        source="Indeed",
                        description=job.get("description", f"{title} at {company}"),
                        salary=salary,
                    )
                )
        logger.info(f"✓ Indeed: {len(jobs)} live jobs fetched")
    except Exception as e:
        logger.error(f"Indeed error: {e}", exc_info=True)
    return jobs


def fetch_internshala(query: str) -> List[Dict]:
    """Internshala jobs via SerpAPI."""
    jobs: List[Dict] = []
    try:
        params = {
            "engine": "google_jobs",
            "q": f"{query} site:internshala.com",
            "location": "India",
            "api_key": SERPAPI_KEY,
        }
        data = _safe_get(SERPAPI_BASE, params)
        if not data or "jobs_results" not in data:
            return jobs
        
        for job in data.get("jobs_results", [])[:8]:
            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("location", "")
            link = job.get("share_link", "") or job.get("link", "")
            salary = job.get("salary", "") or job.get("detected_extensions", {}).get("salary", "Not specified")
            
            if title and link:
                jobs.append(
                    _normalize_job(
                        title=title,
                        company=company,
                        location=location,
                        link=link,
                        source="Internshala",
                        description=job.get("description", title),
                        salary=salary,
                    )
                )
        logger.info(f"✓ Internshala: {len(jobs)} live jobs fetched")
    except Exception as e:
        logger.error(f"Internshala error: {e}", exc_info=True)
    return jobs


def fetch_naukri(query: str) -> List[Dict]:
    """Naukri jobs via SerpAPI."""
    jobs: List[Dict] = []
    try:
        params = {
            "engine": "google_jobs",
            "q": f"{query} site:naukri.com",
            "location": "India",
            "api_key": SERPAPI_KEY,
        }
        data = _safe_get(SERPAPI_BASE, params)
        if not data or "jobs_results" not in data:
            return jobs
        
        for job in data.get("jobs_results", [])[:8]:
            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("location", "")
            link = job.get("share_link", "") or job.get("link", "")
            salary = job.get("salary", "") or job.get("detected_extensions", {}).get("salary", "Not specified")
            
            if title and link:
                jobs.append(
                    _normalize_job(
                        title=title,
                        company=company,
                        location=location,
                        link=link,
                        source="Naukri",
                        description=job.get("description", title),
                        salary=salary,
                    )
                )
        logger.info(f"✓ Naukri: {len(jobs)} live jobs fetched")
    except Exception as e:
        logger.error(f"Naukri error: {e}", exc_info=True)
    return jobs


def fetch_angellist(query: str) -> List[Dict]:
    """Startup jobs via SerpAPI (Wellfound/AngelList)."""
    jobs: List[Dict] = []
    try:
        params = {
            "engine": "google_jobs",
            "q": f"{query} startup India",
            "location": "India",
            "api_key": SERPAPI_KEY,
        }
        data = _safe_get(SERPAPI_BASE, params)
        if not data or "jobs_results" not in data:
            return jobs
        
        for job in data.get("jobs_results", [])[:5]:
            title = job.get("title", "")
            company = job.get("company_name", "")
            location = job.get("location", "")
            link = job.get("share_link", "") or job.get("link", "")
            salary = job.get("salary", "") or job.get("detected_extensions", {}).get("salary", "Not specified")
            
            if title and link:
                jobs.append(
                    _normalize_job(
                        title=title,
                        company=company if company else "Startup",
                        location=location,
                        link=link,
                        source="AngelList",
                        description=job.get("description", title),
                        salary=salary,
                    )
                )
        logger.info(f"✓ Startup Jobs: {len(jobs)} live jobs fetched")
    except Exception as e:
        logger.error(f"Startup Jobs error: {e}", exc_info=True)
    return jobs


def is_cache_valid() -> bool:
    """Check if cache is still valid."""
    if not JOB_CACHE["timestamp"]:
        return False
    return (time.time() - JOB_CACHE["timestamp"]) < JOB_CACHE["expires_in"]


def get_cached_jobs() -> List[Dict]:
    """Get jobs from cache if valid."""
    if is_cache_valid():
        logger.info(f"📦 Cache hit: {len(JOB_CACHE['data'])} jobs")
        return JOB_CACHE["data"]
    return []


def scrape_all_jobs(resume_text: str = None) -> List[Dict]:
    """Scrape all sources in parallel with live data + skill filtering."""
    cached = get_cached_jobs()
    if cached and not resume_text:
        return cached
    
    query = _build_query(resume_text)
    logger.info(f"🕷️ Fetching LIVE jobs for '{query}' via SerpAPI (parallel)...")
    all_jobs = []
    start_time = time.time()
    
    # Parallel execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_google_jobs, query): "Google Jobs",
            executor.submit(fetch_indeed_direct, query): "Indeed Direct",
            executor.submit(fetch_internshala, query): "Internshala",
            executor.submit(fetch_naukri, query): "Naukri",
            executor.submit(fetch_angellist, query): "Startups",
        }
        
        for future in as_completed(futures, timeout=20):
            try:
                jobs = future.result(timeout=18)
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Fetch error: {e}")
    
    elapsed = time.time() - start_time
    
    # De-duplicate (title + company + source)
    unique = {}
    for job in all_jobs:
        key = f"{job.get('title','').lower()}|{job.get('company','').lower()}|{job.get('source','')}"
        if key not in unique:
            unique[key] = job
    all_jobs = list(unique.values())

    # Filter by resume skills if provided
    if resume_text:
        resume_lower = resume_text.lower()
        TECH_SKILLS = ['python', 'java', 'javascript', 'react', 'nodejs', 'fastapi', 'django', 
                       'sql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git', 'linux', 'kotlin']
        matched_skills = [s for s in TECH_SKILLS if s in resume_lower]
        
        filtered_jobs = []
        for job in all_jobs:
            job_skills = job.get("skills", [])
            match_count = sum(1 for skill in matched_skills if skill in job_skills)
            job["relevance_score"] = match_count
            if match_count > 0:
                filtered_jobs.append(job)
        
        filtered_jobs.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        logger.info(f"✓ Filtered to {len(filtered_jobs)} matching jobs in {elapsed:.2f}s")
        all_jobs = filtered_jobs
    
    # Cache results
    JOB_CACHE["data"] = all_jobs
    JOB_CACHE["timestamp"] = time.time()
    logger.info(f"✓ TOTAL: {len(all_jobs)} jobs fetched in {elapsed:.2f}s")
    return all_jobs


def get_jobs_by_source(source: str = None) -> List[Dict]:
    """Get jobs filtered by source."""
    all_jobs = get_cached_jobs() or scrape_all_jobs()
    if source:
        return [j for j in all_jobs if j["source"] == source]
    return all_jobs


def search_jobs(query: str) -> List[Dict]:
    """Search jobs by keyword."""
    all_jobs = get_cached_jobs() or scrape_all_jobs()
    query_lower = query.lower()
    return [j for j in all_jobs if query_lower in j["title"].lower() or query_lower in j["company"].lower()]
