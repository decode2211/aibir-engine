"""
Email & Cover Letter Generator Service
======================================
Generates personalized cold emails and cover letters based on job details and resume.
"""

import re
from typing import Dict, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_skills_from_resume(resume_text: str) -> list:
    """Extract technical skills from resume."""
    if not resume_text:
        return []
    
    COMMON_SKILLS = [
        "python", "java", "javascript", "typescript", "react", "nodejs",
        "fastapi", "django", "flask", "spring", "sql", "mongodb",
        "aws", "docker", "kubernetes", "git", "linux", "c++", "rust",
        "golang", "scala", "kotlin", "php", "ruby", "machine learning",
        "deep learning", "nlp", "computer vision", "data science",
        "api", "rest", "graphql", "microservices", "agile", "scrum"
    ]
    
    resume_lower = resume_text.lower()
    found_skills = [skill for skill in COMMON_SKILLS if skill in resume_lower]
    return list(set(found_skills))  # Remove duplicates


def generate_cold_email(
    job_title: str,
    company_name: str,
    recruiter_name: Optional[str],
    resume_text: str,
    job_description: str,
    user_name: str = "Candidate"
) -> Dict[str, str]:
    """
    Generate a personalized cold email to recruiter.
    
    Args:
        job_title: Title of the job (e.g., "Software Engineer Intern")
        company_name: Company name
        recruiter_name: Name of recruiter (optional)
        resume_text: User's resume content
        job_description: Job description
        user_name: User's name for signature
    
    Returns:
        Dict with subject and body
    """
    
    skills = extract_skills_from_resume(resume_text)
    skills_str = ", ".join(skills[:5]) if skills else "software development"
    
    # Extract key requirements from job description
    key_points = []
    job_desc_lower = job_description.lower()
    
    if "python" in job_desc_lower:
        key_points.append("Python expertise")
    if "react" in job_desc_lower or "frontend" in job_desc_lower:
        key_points.append("Frontend development")
    if "api" in job_desc_lower or "backend" in job_desc_lower:
        key_points.append("Backend systems")
    if "machine learning" in job_desc_lower or "ai" in job_desc_lower:
        key_points.append("AI/ML capabilities")
    if "startup" in job_desc_lower:
        key_points.append("startup agility")
    
    key_points_str = ", ".join(key_points) if key_points else "software development"
    
    salutation = f"Dear {recruiter_name}," if recruiter_name else "Dear Hiring Team,"
    
    subject = f"Excited to Apply for {job_title} @ {company_name}"
    
    body = f"""{salutation}

I came across the {job_title} position at {company_name} and was impressed by your work, especially your focus on {key_points_str.lower()}.

I'm a passionate software engineer with strong skills in {skills_str}. Your job description particularly resonated with me because I'm deeply invested in building scalable solutions and delivering impact quickly.

What excites me about {company_name}:
• Your innovative approach to solving real-world problems
• The opportunity to work with cutting-edge technologies
• A culture that values continuous learning and growth

I'm confident that my technical background and eagerness to contribute would make me a great fit for your team. I'd love to discuss how I can add value to {company_name}.

Could we schedule a brief call at your convenience? I'm flexible with timing and happy to accommodate your schedule.

Thank you for considering my application. I look forward to connecting!

Best regards,
{user_name}

---
📧 Let's connect on professional networks
🔗 Open to: Full-time, Internship, Contract roles
⚡ Availability: Immediate or as per your timeline"""
    
    return {
        "subject": subject,
        "body": body,
        "preview": f"{salutation}\n\n{body.split(chr(10))[2]}"
    }


def generate_cover_letter(
    job_title: str,
    company_name: str,
    resume_text: str,
    job_description: str,
    user_name: str = "Candidate",
    user_email: str = "your.email@example.com",
    user_phone: str = "+91-XXXX-XXXX-XX"
) -> Dict[str, str]:
    """
    Generate a personalized cover letter based on job and resume.
    
    Args:
        job_title: Title of the job
        company_name: Company name
        resume_text: User's resume content
        job_description: Job description
        user_name: User's full name
        user_email: User's email
        user_phone: User's phone number
    
    Returns:
        Dict with formatted cover letter
    """
    
    skills = extract_skills_from_resume(resume_text)
    skills_highlight = skills[:3] if skills else ["Software Development", "Problem Solving", "Collaboration"]
    
    today = datetime.now().strftime("%B %d, %Y")
    
    # Extract company values/culture from description
    company_values = []
    job_desc_lower = job_description.lower()
    
    if "innovation" in job_desc_lower or "innovative" in job_desc_lower:
        company_values.append("innovation and forward-thinking")
    if "impact" in job_desc_lower or "impactful" in job_desc_lower:
        company_values.append("creating tangible impact")
    if "team" in job_desc_lower or "collaboration" in job_desc_lower:
        company_values.append("collaborative teamwork")
    if "growth" in job_desc_lower or "learning" in job_desc_lower:
        company_values.append("continuous growth")
    if "fast-paced" in job_desc_lower or "dynamic" in job_desc_lower:
        company_values.append("fast-paced environments")
    
    company_values_str = " and ".join(company_values) if company_values else "innovation and excellence"
    
    cover_letter = f"""{today}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}. With my passion for technology and proven expertise in {", ".join(skills_highlight)}, I am confident that I can make meaningful contributions to your team.

**Why {company_name}?**

I am particularly drawn to {company_name} because of your commitment to {company_values_str}. Your company's vision aligns perfectly with my career aspirations, and I am excited about the opportunity to contribute to your mission.

**What I Bring:**

Throughout my professional journey, I have developed strong capabilities in:
• {skills_highlight[0]} - delivering high-quality solutions that drive results
• Problem-solving - breaking down complex challenges into manageable tasks
• Collaboration - working effectively with cross-functional teams

I have a proven track record of taking ownership of projects, learning new technologies quickly, and delivering excellence under pressure. My background has equipped me with the skills and mindset needed to excel in the {job_title} role.

**Why I'm a Great Fit:**

The {job_title} position excites me because it combines technical challenges with the opportunity to make a real impact. Your emphasis on {'innovation and scalability' if 'scale' in job_desc_lower else 'quality and reliability'} perfectly matches my approach to software development. I am eager to contribute my expertise while growing alongside your talented team.

**My Commitment:**

I am committed to:
✓ Delivering high-quality code and thoughtful solutions
✓ Being a reliable and proactive team member
✓ Continuously learning and adapting to new technologies
✓ Contributing to a positive and collaborative team culture

I would welcome the opportunity to discuss how my skills and enthusiasm can contribute to {company_name}'s continued success. Thank you for considering my application.

Warm regards,

{user_name}
{user_email}
{user_phone}

---
*Passionate about building innovative solutions | Quick learner | Collaborative team player*"""
    
    return {
        "cover_letter": cover_letter,
        "word_count": len(cover_letter.split()),
        "preview": f"Dear Hiring Manager,\n\nI am writing to express my strong interest in the {job_title} position at {company_name}..."
    }


def generate_email_subject_variations(
    job_title: str,
    company_name: str,
    count: int = 3
) -> list:
    """Generate multiple email subject line variations."""
    variations = [
        f"Excited to apply for {job_title} @ {company_name}",
        f"{job_title} at {company_name} - Let's chat!",
        f"Passionate about {job_title} role at {company_name}",
        f"Quick message: {job_title} opportunity @ {company_name}",
        f"Why I'd be great for {company_name}'s {job_title} position",
        f"Let's discuss {job_title} at {company_name}",
        f"{job_title} @ {company_name} - I'm ready to contribute",
    ]
    return variations[:count]


def generate_follow_up_email(
    recruiter_name: Optional[str],
    company_name: str,
    user_name: str = "Candidate",
    days_since: int = 3
) -> Dict[str, str]:
    """Generate a polite follow-up email."""
    
    salutation = f"Hi {recruiter_name}," if recruiter_name else "Hi there,"
    
    subject = f"Quick follow-up: {company_name} opportunity"
    
    body = f"""{salutation}

I hope this message finds you well! I wanted to follow up on my application for the position at {company_name} that I submitted {days_since} days ago.

I remain very enthusiastic about this opportunity and would love to discuss how I can contribute to your team. If you need any additional information from my side, I'm happy to provide it.

Looking forward to hearing from you!

Best regards,
{user_name}"""
    
    return {
        "subject": subject,
        "body": body,
        "type": "follow_up"
    }
