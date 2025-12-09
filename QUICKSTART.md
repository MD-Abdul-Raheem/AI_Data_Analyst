# ⚡ Quick Start - 5 Minutes to Running

## Step 1: Get Gemini API Key (2 minutes)
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

## Step 2: Setup Backend (2 minutes)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```
GEMINI_API_KEY=paste_your_key_here
```

Start backend:
```bash
python -m backend.main
```

✅ Backend running on http://localhost:8000

## Step 3: Setup Frontend (1 minute)
Open NEW terminal:
```bash
cd frontend
npm install
npm run dev
```

✅ Frontend running on http://localhost:5173

## Step 4: Test It!
1. Open http://localhost:5173
2. Upload `sample_data.csv`
3. Wait 10-20 seconds
4. Explore results!

## Troubleshooting

**"Module not found"**
→ Make sure you're in the correct directory

**"Port already in use"**
→ Kill existing process or change port

**"Gemini API error"**
→ Check your API key is correct in .env

## Next Steps
- Read SETUP.md for detailed instructions
- Read README_V2.md for architecture overview
- Customize prompts in backend/prompts.py
- Modify UI in frontend/src/components/

## Windows Users
Just double-click:
- `run_backend.bat` (starts backend)
- `run_frontend.bat` (starts frontend)

That's it! 🎉
