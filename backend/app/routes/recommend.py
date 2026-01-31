from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.services.data_store import get_student
from app.core.orchestrator import generate_recommendations

router = APIRouter(prefix="/recommend")

@router.get("/{student_id}", response_model=Dict[str, Any])
def recommend(student_id: str):
    student = get_student(student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    recommendations = generate_recommendations(student["resume_text"])
    return recommendations
