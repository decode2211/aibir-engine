from app.core.ml_engine import extract_skills_from_text
from app.services.web_scraper import scrape_all_jobs

def generate_recommendations(resume_text: str):
    """
    Returns REAL jobs matching student skills
    """
    
    # Extract detected skills from resume
    detected_skills = extract_skills_from_text(resume_text)
    
    # Scrape jobs filtered by resume skills
    all_jobs = scrape_all_jobs(resume_text=resume_text)
    
    # Format results with full job details
    internships = [
        {
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location", "India"),
            "salary": job.get("salary", "Not specified"),
            "description": job.get("description"),
            "source": job.get("source", "Unknown"),
            "link": job.get("link"),
            "deadline": job.get("deadline"),
            "skills_needed": job.get("skills", []),
            "relevance": job.get("relevance_score", 0),
        }
        for job in all_jobs
    ]
    
    return {
        "internships": internships,
        "skills_detected": detected_skills,
        "total_count": len(internships),
        "sources": list(set(job["source"] for job in all_jobs)),
        "message": f"Found {len(internships)} jobs matching your skills!"
    }
