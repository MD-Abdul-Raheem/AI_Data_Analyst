from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os
import uuid
from pathlib import Path
from .database import init_db, get_session, Job
from .orchestrator import Orchestrator
from .utils import clean_for_json
import json

app = FastAPI(title="AI Data Analyst API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./uploads"))
UPLOAD_DIR.mkdir(exist_ok=True)

orchestrator = Orchestrator()

@app.on_event("startup")
async def startup():
    await init_db()

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    session: AsyncSession = Depends(get_session)
):
    """Upload file and start analysis"""
    # Validate file
    if not file.filename.endswith(('.csv', '.xlsx', '.xls', '.json')):
        raise HTTPException(400, "Unsupported file format")
    
    # Create job
    job_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create job record
    job = Job(id=job_id, filename=file.filename, status="pending")
    session.add(job)
    await session.commit()
    
    # Start background processing
    background_tasks.add_task(orchestrator.process_job, job_id, str(file_path), file.filename)
    
    return {"job_id": job_id, "status": "pending"}

@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str, session: AsyncSession = Depends(get_session)):
    """Get job status and result"""
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(404, "Job not found")
    
    response = {
        "id": job.id,
        "filename": job.filename,
        "status": job.status,
        "created_at": job.created_at.isoformat(),
        "rows": job.rows,
        "columns": job.columns,
        "quality_score": job.quality_score
    }
    
    if job.status == "completed" and job.result_json:
        response["result"] = json.loads(job.result_json)
    elif job.status == "failed":
        response["error"] = job.error_message
    
    return response

@app.post("/api/download/notebook")
async def download_notebook(data: dict):
    """Download Jupyter notebook"""
    notebook = data.get("notebook")
    if not notebook:
        raise HTTPException(400, "No notebook data")
    
    file_path = UPLOAD_DIR / f"analysis_{uuid.uuid4()}.ipynb"
    with open(file_path, "w") as f:
        json.dump(clean_for_json(notebook), f, indent=2)
    
    return FileResponse(file_path, filename="analysis.ipynb", media_type="application/json")

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
