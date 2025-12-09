# ✅ Setup Checklist - AI Data Analyst V2

## Prerequisites
- [ ] Python 3.8+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed (optional)
- [ ] Text editor (VS Code recommended)

## Get API Key
- [ ] Go to https://makersuite.google.com/app/apikey
- [ ] Create Google account (if needed)
- [ ] Click "Create API Key"
- [ ] Copy API key to clipboard

## Backend Setup
- [ ] Open terminal
- [ ] Navigate to project: `cd "AI Data Analyst VS code"`
- [ ] Go to backend: `cd backend`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate venv: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create .env file: `copy .env.example .env` (Windows) or `cp .env.example .env` (Mac/Linux)
- [ ] Edit .env and paste your Gemini API key
- [ ] Test backend: `python -m backend.main`
- [ ] Verify: Open http://localhost:8000/api/health in browser
- [ ] Should see: `{"status": "ok"}`

## Frontend Setup
- [ ] Open NEW terminal (keep backend running)
- [ ] Navigate to project: `cd "AI Data Analyst VS code"`
- [ ] Go to frontend: `cd frontend`
- [ ] Install dependencies: `npm install`
- [ ] Start frontend: `npm run dev`
- [ ] Verify: Open http://localhost:5173 in browser
- [ ] Should see: Upload interface

## First Test
- [ ] Keep both terminals running
- [ ] Open http://localhost:5173
- [ ] Click "Choose File" or drag & drop
- [ ] Select `sample_data.csv` from project root
- [ ] Wait 10-20 seconds
- [ ] Verify: Results appear in tabs
- [ ] Click through all 6 tabs:
  - [ ] Summary (shows metrics)
  - [ ] Insights (AI-generated text)
  - [ ] Charts (images display)
  - [ ] Python (code displays)
  - [ ] SQL (queries display)
  - [ ] DAX (measures display)
- [ ] Click "Download Notebook"
- [ ] Verify: analysis.ipynb downloads
- [ ] Open notebook in Jupyter/VS Code
- [ ] Verify: Notebook has cells with code

## Troubleshooting

### Backend Issues
- [ ] "Module not found" → Check you're in backend/ directory
- [ ] "Port 8000 in use" → Kill existing process or change port
- [ ] "Gemini API error" → Check API key in .env file
- [ ] "Database error" → Delete jobs.db and restart

### Frontend Issues
- [ ] "npm not found" → Install Node.js
- [ ] "Port 5173 in use" → Kill existing process
- [ ] "Cannot connect to backend" → Verify backend is running on port 8000
- [ ] "CORS error" → Check CORS settings in backend/main.py

### Upload Issues
- [ ] "Unsupported format" → Use CSV, Excel, or JSON only
- [ ] "File too large" → Max 500MB (change in .env)
- [ ] "Processing stuck" → Check backend terminal for errors
- [ ] "No results" → Check backend logs, verify Gemini API key

## Verification Tests

### Test 1: Small Dataset
- [ ] Upload sample_data.csv (30 rows)
- [ ] Processing time: < 15 seconds
- [ ] All tabs populate
- [ ] Download works

### Test 2: Medium Dataset
- [ ] Create CSV with 10,000 rows
- [ ] Upload and verify
- [ ] Processing time: < 30 seconds
- [ ] Charts generate correctly

### Test 3: Different Formats
- [ ] Test CSV upload
- [ ] Test Excel (.xlsx) upload
- [ ] Test JSON upload
- [ ] All formats work

### Test 4: Error Handling
- [ ] Upload invalid file (e.g., .txt)
- [ ] Verify error message displays
- [ ] Upload empty file
- [ ] Verify error handling

## Optional Enhancements

### Windows Users
- [ ] Test `run_backend.bat`
- [ ] Test `run_frontend.bat`
- [ ] Create desktop shortcuts

### Development
- [ ] Install VS Code extensions:
  - [ ] Python
  - [ ] Pylance
  - [ ] ES7+ React snippets
  - [ ] Prettier
- [ ] Configure linting
- [ ] Set up debugging

### Production
- [ ] Set up PostgreSQL
- [ ] Configure nginx
- [ ] Set up HTTPS
- [ ] Add authentication
- [ ] Set up monitoring
- [ ] Configure backups

## Documentation Review
- [ ] Read README_V2.md (overview)
- [ ] Read SETUP.md (detailed setup)
- [ ] Read QUICKSTART.md (quick reference)
- [ ] Read MIGRATION_V1_TO_V2.md (if migrating)
- [ ] Read IMPLEMENTATION_SUMMARY.md (architecture)

## Next Steps
- [ ] Customize prompts in backend/prompts.py
- [ ] Modify UI colors in frontend/src/components/
- [ ] Add custom analysis logic
- [ ] Implement additional features
- [ ] Deploy to production

## Success Criteria
✅ All items checked = Ready to use!

## Support
- Issues with setup? → Check SETUP.md
- Questions about features? → Check README_V2.md
- Need quick help? → Check QUICKSTART.md
- Migrating from V1? → Check MIGRATION_V1_TO_V2.md

---

**Once all items are checked, you're ready to analyze data! 🎉**
