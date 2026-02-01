"""
Email & Cover Letter Generation Endpoints
==========================================
Provides endpoints for generating cold emails and cover letters.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.email_cover_letter_generator import (
    generate_cold_email,
    generate_cover_letter,
    generate_email_subject_variations,
    generate_follow_up_email,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/generate", tags=["Generate"])


class EmailRequest(BaseModel):
    job_title: str
    company_name: str
    recruiter_name: Optional[str] = None
    resume_text: str
    job_description: str
    user_name: str = "Candidate"


class CoverLetterRequest(BaseModel):
    job_title: str
    company_name: str
    resume_text: str
    job_description: str
    user_name: str = "Candidate"
    user_email: str = "your.email@example.com"
    user_phone: str = "+91-XXXX-XXXX-XX"


class FollowUpEmailRequest(BaseModel):
    recruiter_name: Optional[str] = None
    company_name: str
    user_name: str = "Candidate"
    days_since: int = 3


@router.post("/email")
async def generate_email(request: EmailRequest):
    """Generate a personalized cold email for a job application."""
    try:
        email_data = generate_cold_email(
            job_title=request.job_title,
            company_name=request.company_name,
            recruiter_name=request.recruiter_name,
            resume_text=request.resume_text,
            job_description=request.job_description,
            user_name=request.user_name,
        )
        
        logger.info(f"✓ Generated cold email for {request.job_title} @ {request.company_name}")
        
        return {
            "status": "success",
            "data": email_data,
        }
    except Exception as e:
        logger.error(f"Email generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Email generation failed: {str(e)}")


@router.post("/cover-letter")
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """Generate a personalized cover letter for a job application."""
    try:
        cover_letter_data = generate_cover_letter(
            job_title=request.job_title,
            company_name=request.company_name,
            resume_text=request.resume_text,
            job_description=request.job_description,
            user_name=request.user_name,
            user_email=request.user_email,
            user_phone=request.user_phone,
        )
        
        logger.info(f"✓ Generated cover letter for {request.job_title} @ {request.company_name}")
        
        return {
            "status": "success",
            "data": cover_letter_data,
        }
    except Exception as e:
        logger.error(f"Cover letter generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Cover letter generation failed: {str(e)}")


@router.get("/email-subjects")
async def get_email_subjects(job_title: str, company_name: str, count: int = 3):
    """Get multiple email subject line variations."""
    try:
        subjects = generate_email_subject_variations(
            job_title=job_title,
            company_name=company_name,
            count=min(count, 5)  # Limit to 5 max
        )
        
        logger.info(f"✓ Generated {len(subjects)} email subject variations")
        
        return {
            "status": "success",
            "data": {
                "subjects": subjects,
                "count": len(subjects),
            }
        }
    except Exception as e:
        logger.error(f"Subject generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Subject generation failed: {str(e)}")


@router.post("/follow-up-email")
async def generate_followup(request: FollowUpEmailRequest):
    """Generate a follow-up email for a previous application."""
    try:
        email_data = generate_follow_up_email(
            recruiter_name=request.recruiter_name,
            company_name=request.company_name,
            user_name=request.user_name,
            days_since=request.days_since,
        )
        
        logger.info(f"✓ Generated follow-up email for {request.company_name}")
        
        return {
            "status": "success",
            "data": email_data,
        }
    except Exception as e:
        logger.error(f"Follow-up email generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Follow-up email generation failed: {str(e)}")
