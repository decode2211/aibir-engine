from fastapi import FastAPI
from app.config import setup_cors
from app.routes import resume, recommend

app = FastAPI(title="AIBIR Backend")

setup_cors(app)

app.include_router(resume.router)
app.include_router(recommend.router)

@app.get("/")
def root():
    return {"message": "AIBIR Backend is running 🚀"}
