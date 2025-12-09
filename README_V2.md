# 🤖 AI Data Analyst V2 - FastAPI + React + Gemini AI

**Professional Data Analysis Platform with LLM-Powered Insights**

## 🎯 What's New in V2?

### Architecture Upgrade
- **Backend**: Flask → **FastAPI** (async, faster, modern)
- **Frontend**: HTML/JS → **React + Vite** (component-based, reactive)
- **AI Integration**: **Google Gemini API** for intelligent insights
- **Database**: **SQLite** for job tracking and persistence
- **Processing**: **Async background jobs** with real-time polling

### New Features
✅ **LLM-Generated Insights** - AI-powered business recommendations  
✅ **Async Job Processing** - Non-blocking analysis for large files  
✅ **Real-Time Status Updates** - Live progress tracking  
✅ **Advanced Data Profiling** - Quality scores, cardinality analysis  
✅ **Base64 Charts** - No file storage needed  
✅ **Modern React UI** - Fast, responsive, professional  
✅ **Job History** - SQLite database tracks all analyses  

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Create .env file with your Gemini API key
echo GEMINI_API_KEY=your_key_here > .env

python -m backend.main
```

### 2. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Open Browser
Navigate to **http://localhost:5173**

## 📁 Project Structure

```
AI Data Analyst VS code/
│
├── backend/                    # FastAPI Backend
│   ├── main.py                # API endpoints
│   ├── database.py            # SQLite models
│   ├── orchestrator.py        # Workflow manager
│   ├── llm.py                 # Gemini AI integration
│   ├── prompts.py             # LLM prompt templates
│   ├── profiler.py            # Data profiling
│   ├── analysis.py            # Pandas + charts
│   ├── exporter.py            # File generation
│   ├── utils.py               # Helpers
│   └── requirements.txt       # Python deps
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx    # File upload
│   │   │   └── Dashboard.jsx     # Results display
│   │   ├── services/
│   │   │   └── api.js            # API client
│   │   ├── App.jsx               # Main app
│   │   └── main.jsx              # Entry point
│   ├── package.json
│   └── vite.config.js
│
├── SETUP.md                    # Detailed setup guide
├── run_backend.bat             # Windows backend launcher
└── run_frontend.bat            # Windows frontend launcher
```

## 🔄 How It Works

### Workflow
```
1. User uploads file → Frontend sends to /api/upload
2. Backend creates Job in SQLite, saves file
3. Background task starts orchestrator
4. Orchestrator runs:
   - Data profiling (quality, cardinality)
   - Data cleaning (missing values, duplicates)
   - EDA analysis (stats, correlations)
   - Chart generation (matplotlib → base64)
   - LLM calls (Gemini API for insights/code)
5. Results saved to Job.result_json
6. Frontend polls /api/jobs/{id} every 2 seconds
7. When complete, displays results in tabs
```

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/upload` | POST | Upload file, create job |
| `/api/jobs/{id}` | GET | Get job status & results |
| `/api/download/notebook` | POST | Download Jupyter notebook |
| `/api/health` | GET | Health check |

## 🤖 LLM Integration

### Gemini API Features
- **Insights Generation**: Analyzes data profile and generates business insights
- **SQL Query Generation**: Creates useful queries based on schema
- **Python Code Generation**: Produces complete analysis scripts
- **DAX Measures**: Generates Power BI calculations

### Prompt Templates
Located in `backend/prompts.py`:
- `INSIGHTS_PROMPT` - Business insights
- `SQL_PROMPT` - Database queries
- `PYTHON_PROMPT` - Analysis code
- `DAX_PROMPT` - BI measures

## 📊 Features Comparison

| Feature | V1 (Flask) | V2 (FastAPI + React) |
|---------|-----------|---------------------|
| Backend | Flask (sync) | FastAPI (async) |
| Frontend | HTML/JS | React + Vite |
| AI | None | Gemini API |
| Processing | Blocking | Background jobs |
| Database | None | SQLite |
| Charts | File storage | Base64 inline |
| UI Updates | Page reload | Real-time polling |
| Job Tracking | No | Yes |

## 🔧 Configuration

### Backend (.env)
```env
GEMINI_API_KEY=your_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./jobs.db
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=524288000
```

### Frontend (vite.config.js)
```js
server: {
  port: 5173,
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Manual Testing
1. Upload `sample_data.csv`
2. Verify job status updates
3. Check all tabs display correctly
4. Download notebook and verify format
5. Test with large file (100MB+)

## 🚀 Production Deployment

### Backend
```bash
# Using Gunicorn + Uvicorn workers
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
npm run build
# Serve dist/ with nginx or Vercel
```

### Environment
- Set `GEMINI_API_KEY` in production environment
- Use PostgreSQL instead of SQLite for production
- Enable HTTPS
- Add rate limiting
- Implement authentication

## 📈 Performance

| Dataset Size | Processing Time | Status Updates |
|--------------|----------------|----------------|
| < 10K rows | 5-10 seconds | Every 2 seconds |
| 10K-100K rows | 10-30 seconds | Every 2 seconds |
| 100K-1M rows | 30-120 seconds | Every 2 seconds |

## 🔒 Security

- File type validation (CSV, Excel, JSON only)
- File size limits (500MB default)
- Async processing prevents blocking
- CORS configured for localhost
- Input sanitization
- Temporary file cleanup

## 🆘 Troubleshooting

**Backend won't start**
- Check Python version (3.8+)
- Verify virtual environment is activated
- Ensure all dependencies installed

**Frontend won't start**
- Check Node version (18+)
- Run `npm install` again
- Clear node_modules and reinstall

**Gemini API errors**
- Verify API key is valid
- Check quota limits
- Ensure internet connection

**CORS errors**
- Verify backend runs on port 8000
- Verify frontend runs on port 5173
- Check CORS middleware in main.py

## 📚 Documentation

- **SETUP.md** - Detailed setup instructions
- **API_DOCUMENTATION.md** - API reference (V1)
- **USAGE_GUIDE.md** - User guide (V1)
- **README.md** - Original V1 documentation

## 🎓 Learning Resources

### FastAPI
- https://fastapi.tiangolo.com/
- Async programming in Python
- Background tasks

### React
- https://react.dev/
- Component lifecycle
- State management

### Gemini API
- https://ai.google.dev/
- Prompt engineering
- API limits

## 🤝 Contributing

Areas for improvement:
- [ ] Add user authentication
- [ ] Implement caching
- [ ] Add more chart types
- [ ] Support more file formats
- [ ] Add data export options
- [ ] Implement snapshot testing
- [ ] Add unit tests
- [ ] Create Docker setup

## 📄 License

Open Source - Free for personal and commercial use

---

**Built with ❤️ using FastAPI, React, and Google Gemini AI**

**Transform any dataset into actionable insights instantly!**
