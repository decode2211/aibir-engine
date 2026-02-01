from fastapi import APIRouter, UploadFile, Form, File
from app.services.resume_parser import extract_text_from_pdf
from app.services.data_store import create_student

router = APIRouter(prefix="/resume")

@router.post("/upload")
async def upload_resume(
    resume: UploadFile = File(...),
    student_name: str = Form(...),
    student_email: str = Form(...)
):
    text = extract_text_from_pdf(resume.file)

    student_id = create_student({
        "name": student_name,
        "email": student_email,
        "resume_text": text
    })

    return {
        "student_id": student_id,
        "message": "Resume processed using AI"
    }
