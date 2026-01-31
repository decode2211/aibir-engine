from pydantic import BaseModel
from typing import List

class UploadResponse(BaseModel):
    student_id: str
    message: str

class InternshipRecommendation(BaseModel):
    title: str
    company: str
    match_percentage: float
    required_skills: List[str]
    explanation: str
    apply_link: str
    location: str
    duration: str
    stipend: str
