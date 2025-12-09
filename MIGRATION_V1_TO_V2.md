# 🔄 Migration Guide: V1 (Flask) → V2 (FastAPI + React)

## What Changed?

### Architecture
| Component | V1 | V2 |
|-----------|----|----|
| Backend | Flask (sync) | FastAPI (async) |
| Frontend | Jinja templates | React SPA |
| Processing | Synchronous | Background jobs |
| Database | None | SQLite |
| AI | None | Gemini API |

### File Structure
```
V1:
├── app.py (500+ lines)
├── templates/index.html (800+ lines)
└── config.py

V2:
├── backend/
│   ├── main.py (API)
│   ├── orchestrator.py (workflow)
│   ├── llm.py (AI)
│   └── ... (modular)
└── frontend/
    └── src/ (React components)
```

## Key Differences

### 1. File Upload
**V1**: Synchronous, blocks until complete
```python
@app.route('/analyze', methods=['POST'])
def analyze():
    # Blocks for entire analysis
    result = analyst.analyze()
    return jsonify(result)
```

**V2**: Async, returns immediately
```python
@app.post("/api/upload")
async def upload_file(background_tasks: BackgroundTasks):
    # Returns job_id immediately
    background_tasks.add_task(orchestrator.process_job, job_id)
    return {"job_id": job_id}
```

### 2. Status Updates
**V1**: No status updates, user waits
**V2**: Real-time polling every 2 seconds

### 3. Results Display
**V1**: Server-side rendering (Jinja)
**V2**: Client-side rendering (React)

### 4. AI Integration
**V1**: Rule-based insights
**V2**: LLM-generated insights via Gemini

## Migration Steps

### Option A: Keep Both (Recommended)
1. Keep V1 in `app.py` and `templates/`
2. Run V2 alongside in `backend/` and `frontend/`
3. V1 on port 5000, V2 on ports 8000/5173

### Option B: Full Migration
1. Backup V1 files
2. Test V2 thoroughly
3. Update documentation
4. Switch production traffic

## Feature Parity

| Feature | V1 | V2 | Notes |
|---------|----|----|-------|
| CSV Upload | ✅ | ✅ | Same |
| Excel Upload | ✅ | ✅ | Same |
| JSON Upload | ✅ | ✅ | Same |
| Data Cleaning | ✅ | ✅ | Same logic |
| EDA | ✅ | ✅ | Same |
| Python Code | ✅ | ✅ | LLM-enhanced |
| SQL Queries | ✅ | ✅ | LLM-generated |
| DAX Measures | ✅ | ✅ | LLM-generated |
| Notebook | ✅ | ✅ | Same format |
| Insights | ✅ | ✅ | **AI-powered in V2** |
| Charts | ✅ | ✅ | Base64 in V2 |
| Job Tracking | ❌ | ✅ | **New in V2** |
| Status Updates | ❌ | ✅ | **New in V2** |

## Code Comparison

### Data Profiling
**V1**: In DataAnalyst class
**V2**: Separate DataProfiler class with quality scoring

### Analysis
**V1**: Synchronous in single class
**V2**: Async orchestrator coordinates multiple services

### Charts
**V1**: Saved to files
**V2**: Base64 encoded, no file storage

## API Changes

### V1 Endpoints
```
POST /analyze → Returns full result
POST /download/notebook → Downloads notebook
```

### V2 Endpoints
```
POST /api/upload → Returns job_id
GET /api/jobs/{id} → Returns status + result
POST /api/download/notebook → Downloads notebook
```

## Configuration

### V1
```python
# config.py
MAX_CONTENT_LENGTH = 500 * 1024 * 1024
```

### V2
```env
# .env
GEMINI_API_KEY=your_key
MAX_FILE_SIZE=524288000
```

## Testing

### V1
```bash
python test_app.py
```

### V2
```bash
cd backend
pytest test_basic.py
```

## Deployment

### V1
```bash
python app.py
# or
gunicorn app:app
```

### V2
```bash
# Backend
uvicorn backend.main:app --workers 4

# Frontend
npm run build
# Serve dist/ folder
```

## Advantages of V2

1. **Scalability**: Async processing handles more concurrent users
2. **Modularity**: Easier to maintain and extend
3. **AI-Powered**: Gemini generates smarter insights
4. **Modern UI**: React provides better UX
5. **Job Tracking**: SQLite stores analysis history
6. **Real-Time**: Live status updates
7. **Type Safety**: FastAPI provides automatic validation

## When to Use V1 vs V2

### Use V1 if:
- Simple deployment needed
- No AI features required
- Single-user environment
- Quick prototype

### Use V2 if:
- Production deployment
- Multiple concurrent users
- AI-powered insights needed
- Modern UI required
- Job history tracking needed

## Backward Compatibility

V2 maintains same output formats:
- Jupyter notebooks are compatible
- JSON structure is similar
- Python code format unchanged
- SQL queries format unchanged

## Support

Both versions will be maintained:
- **V1**: Bug fixes only
- **V2**: Active development

## Questions?

- V1 Issues: Check original README.md
- V2 Issues: Check README_V2.md and SETUP.md
- General: Check QUICKSTART.md

---

**Recommendation**: Start new projects with V2, migrate existing projects gradually.
