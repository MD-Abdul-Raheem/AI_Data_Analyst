# 🚀 Setup Guide - AI Data Analyst (FastAPI + React)

## Prerequisites
- Python 3.8+
- Node.js 18+
- Gemini API Key (get from https://makersuite.google.com/app/apikey)

## Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Run backend
python -m backend.main
# Backend runs on http://localhost:8000
```

## Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run frontend
npm run dev
# Frontend runs on http://localhost:5173
```

## Quick Start

1. **Start Backend**: `cd backend && python -m backend.main`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Open Browser**: http://localhost:5173
4. **Upload Dataset**: Drag & drop CSV/Excel/JSON file
5. **View Results**: Explore insights, charts, code

## Environment Variables

Create `backend/.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./jobs.db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=524288000
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Production Deployment

### Backend (FastAPI)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend (React)
```bash
npm run build
# Serve dist/ folder with nginx or similar
```

## Troubleshooting

**Issue**: Module not found errors
**Fix**: Ensure you're in the correct directory and virtual environment is activated

**Issue**: CORS errors
**Fix**: Check that backend is running on port 8000 and frontend on 5173

**Issue**: Gemini API errors
**Fix**: Verify your API key is valid and has quota remaining

## Architecture

```
Backend (FastAPI) :8000
├── /api/upload → Create job, start processing
├── /api/jobs/{id} → Poll status, get results
└── /api/download/notebook → Download .ipynb

Frontend (React) :5173
├── UploadZone → File upload + progress
├── Dashboard → Results display
└── API Service → Polling logic
```

## Features

✅ Async job processing with SQLite tracking
✅ LLM-powered insights via Gemini API
✅ Base64 chart generation (no file storage)
✅ Real-time polling for job status
✅ Professional React UI with tabs
✅ Downloadable Jupyter notebooks
