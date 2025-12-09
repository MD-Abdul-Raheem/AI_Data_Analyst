# 📦 Installation Guide

## Prerequisites

Before installing, ensure you have:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for API calls)

## Step-by-Step Installation

### 1. Verify Node.js Installation

```bash
node --version
# Should show v16.0.0 or higher

npm --version
# Should show 8.0.0 or higher
```

### 2. Navigate to Project Directory

```bash
cd "c:\Users\mdabd\Documents\AI Data Analyst Cloud\advanced-analyst"
```

### 3. Install Dependencies

```bash
npm install
```

This will install:
- React 18.2.0
- Lucide React (icons)
- PapaCSV (CSV parsing)
- SheetJS (Excel handling)
- Recharts (visualizations)
- Math.js (statistics)
- React Syntax Highlighter (code display)
- Vite (build tool)
- Tailwind CSS (styling)

**Installation time**: 2-5 minutes depending on internet speed

### 4. Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v4.3.9  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### 5. Open in Browser

Navigate to: `http://localhost:3000`

## Troubleshooting

### Issue: "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Issue: Port 3000 already in use
**Solution**: 
```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use different port
npm run dev -- --port 3001
```

### Issue: Dependencies installation fails
**Solution**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: API errors
**Solution**: Check internet connection and verify Gemini API key is valid

## Building for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

Build output will be in `dist/` folder.

## Deployment Options

### 1. Netlify
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod
```

### 2. Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### 3. GitHub Pages
```bash
# Build
npm run build

# Deploy dist folder to gh-pages branch
```

## Environment Variables (Optional)

Create `.env` file in project root:

```env
VITE_GEMINI_API_KEY=your_api_key_here
```

Update `App.jsx`:
```javascript
const GEMINI_API_KEY = import.meta.env.VITE_GEMINI_API_KEY;
```

## System Requirements

### Minimum
- 4GB RAM
- 2 CPU cores
- 500MB free disk space
- Modern browser (last 2 versions)

### Recommended
- 8GB RAM
- 4 CPU cores
- 1GB free disk space
- Chrome/Edge (latest version)

## Next Steps

After successful installation:
1. Read [README.md](README.md) for feature overview
2. Upload a sample CSV file to test
3. Explore all analysis tabs
4. Try different datasets

## Support

If you encounter issues:
1. Check Node.js and npm versions
2. Verify all dependencies installed correctly
3. Check browser console for errors
4. Ensure internet connection is stable

---

**Installation complete! 🎉**

Start analyzing data with: `npm run dev`
