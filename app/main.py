from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from .agent import analyze_complaint
from .cache import get_cached_response, set_cached_response
from .database import save_complaint, create_tables

app = FastAPI(title="AI Customer Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
create_tables()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "AI Customer Support Agent is running"}

@app.post("/analyze")
async def analyze(
    complaint: str = Form(...),
    image: UploadFile = File(...)
):
    # Save uploaded image
    image_path = f"{UPLOAD_DIR}/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Check cache first
    cached = get_cached_response(complaint, image_path)
    if cached:
        return {
            "response": cached,
            "source": "cache",
            "complaint": complaint
        }

    # Call AI agent
    response = analyze_complaint(image_path, complaint)

    # Save to cache
    set_cached_response(complaint, image_path, response)

    # Save to database
    save_complaint(complaint, image_path, response)

    return {
        "response": response,
        "source": "ai",
        "complaint": complaint
    }

@app.get("/complaints")
def get_complaints():
    from .database import get_all_complaints
    complaints = get_all_complaints()
    return {
        "total": len(complaints),
        "complaints": [
            {
                "id": c.id,
                "complaint": c.complaint_text,
                "response": c.ai_response,
                "status": c.status,
                "created_at": str(c.created_at)
            }
            for c in complaints
        ]
    }