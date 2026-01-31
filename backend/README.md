# backend

This folder contains the FastAPI backend for aibir-engine. Structure:

- `app/main.py` - FastAPI entry point
- `app/config.py` - CORS & basic settings
- `app/models/schemas.py` - Pydantic request/response schemas
- `app/routes/resume.py` - `/upload-resume` endpoint
- `app/routes/recommend.py` - `/recommend/{student_id}` endpoint
- `app/services/*` - helper services (parser, ai engine, data store)
- `app/data/internships.json` - sample dataset

Run with:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --factory
```
