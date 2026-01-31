from app.core.ml_engine import extract_skills_from_text
from app.services.realtime_internships import fetch_linkedin_jobs

def generate_recommendations(resume_text: str):
    """
    Returns only LinkedIn real-time internships
    """
    
    # Extract detected skills from resume
    detected_skills = extract_skills_from_text(resume_text)
    
    # Fetch LinkedIn internships only
    linkedin_internships = fetch_linkedin_jobs(detected_skills, location="India", limit=20)
    
    # Format results
    internships = [
        {
            "title": internship.get("title"),
            "company": internship.get("company"),
            "location": internship.get("location", "India"),
            "source": "LinkedIn",
            "skills": internship.get("skills", detected_skills[:3]),
            "url": internship.get("url", "https://linkedin.com/jobs"),
            "type": internship.get("type", "internship")
        }
        for internship in linkedin_internships
    ]
    
    return {
        "internships": internships,
        "skills": detected_skills,
        "total_count": len(internships)
    }
