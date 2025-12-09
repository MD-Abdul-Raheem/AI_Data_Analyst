# 🔧 AI Data Analyst - Installation Guide

## Prerequisites

Before installing, ensure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- **Web browser** (Chrome, Firefox, Edge, Safari)
- **Internet connection** (for downloading packages)

---

## Installation Methods

### Method 1: Quick Install (Recommended)

#### Windows

```bash
# 1. Open Command Prompt or PowerShell
# Navigate to project folder
cd "C:\Users\mdabd\Documents\AI Data Analyst VS code"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py

# 4. Open browser to http://localhost:5000
```

**Or simply double-click:** `run.bat`

#### macOS / Linux

```bash
# 1. Open Terminal
# Navigate to project folder
cd "/path/to/AI Data Analyst VS code"

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run the application
python3 app.py

# 4. Open browser to http://localhost:5000
```

---

### Method 2: Virtual Environment (Best Practice)

#### Windows

```bash
# 1. Navigate to project folder
cd "C:\Users\mdabd\Documents\AI Data Analyst VS code"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py
```

#### macOS / Linux

```bash
# 1. Navigate to project folder
cd "/path/to/AI Data Analyst VS code"

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
python app.py
```

---

## Verifying Installation

### Step 1: Check Python Version

```bash
python --version
# Should show: Python 3.8.x or higher
```

### Step 2: Check pip

```bash
pip --version
# Should show pip version
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Collecting Flask==3.0.0
Collecting pandas==2.1.4
Collecting numpy==1.26.2
...
Successfully installed Flask-3.0.0 pandas-2.1.4 ...
```

### Step 4: Run Test Suite

```bash
# Start the server first
python app.py

# In another terminal, run tests
python test_app.py
```

Expected output:
```
============================================================
  AI DATA ANALYST - TEST SUITE
============================================================

✓ Server is running
✓ Analysis completed in 2.34 seconds
✓ All tests passed!
```

---

## Troubleshooting Installation

### Issue 1: Python Not Found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart terminal/command prompt
4. Try again

---

### Issue 2: pip Not Found

**Error:**
```
'pip' is not recognized as an internal or external command
```

**Solution:**
```bash
# Windows
python -m ensurepip --upgrade

# macOS/Linux
python3 -m ensurepip --upgrade
```

---

### Issue 3: Permission Denied

**Error:**
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Option 1: Use --user flag
pip install --user -r requirements.txt

# Option 2: Use virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

---

### Issue 4: Package Installation Fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solution:**
```bash
# Update pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt

# If still fails, install packages individually
pip install Flask
pip install pandas
pip install numpy
pip install matplotlib
pip install seaborn
pip install scipy
pip install openpyxl
```

---

### Issue 5: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Option 1: Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Option 2: Use different port
# Edit app.py, change last line to:
app.run(debug=True, port=5001)
```

---

### Issue 6: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure you're in the correct environment
# If using virtual environment, activate it first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Then install
pip install -r requirements.txt
```

---

## Dependency Details

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| pandas | 2.1.4 | Data manipulation |
| numpy | 1.26.2 | Numerical computing |
| matplotlib | 3.8.2 | Plotting |
| seaborn | 0.13.0 | Statistical viz |
| scipy | 1.11.4 | Scientific computing |
| openpyxl | 3.1.2 | Excel support |
| Werkzeug | 3.0.1 | WSGI utilities |

### Total Size
Approximately **500-800 MB** (including all dependencies)

### Installation Time
- **Fast internet**: 2-5 minutes
- **Slow internet**: 5-15 minutes

---

## Platform-Specific Notes

### Windows
- Use Command Prompt or PowerShell
- Backslashes in paths: `C:\Users\...`
- Use `python` and `pip` commands
- Can use `run.bat` for easy startup

### macOS
- Use Terminal
- Forward slashes in paths: `/Users/...`
- Use `python3` and `pip3` commands
- May need to install Xcode Command Line Tools

### Linux
- Use Terminal
- Forward slashes in paths: `/home/...`
- Use `python3` and `pip3` commands
- May need to install python3-dev package

---

## Post-Installation Setup

### 1. Test with Sample Data

```bash
# Start server
python app.py

# Open browser
http://localhost:5000

# Upload sample_data.csv
# Verify analysis completes successfully
```

### 2. Configure Settings (Optional)

Edit `config.py` to customize:
- Upload folder location
- Maximum file size
- Analysis parameters
- Visualization settings

### 3. Create Desktop Shortcut (Optional)

#### Windows
1. Right-click `run.bat`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Rename to "AI Data Analyst"

#### macOS
1. Create file `start.command`:
```bash
#!/bin/bash
cd "/path/to/AI Data Analyst VS code"
python3 app.py
```
2. Make executable: `chmod +x start.command`
3. Double-click to run

---

## Updating the Application

### Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade pandas
```

### Update Application Files

```bash
# If you have updates to app.py or other files
# Simply replace the files and restart the server
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate if active
deactivate

# Delete venv folder
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

### Remove Dependencies

```bash
# If not using virtual environment
pip uninstall -r requirements.txt -y
```

### Remove Application

Simply delete the project folder

---

## Docker Installation (Advanced)

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Build and Run

```bash
# Build image
docker build -t ai-data-analyst .

# Run container
docker run -p 5000:5000 ai-data-analyst

# Open browser to http://localhost:5000
```

---

## Cloud Deployment

### Heroku

```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create ai-data-analyst
git push heroku main
```

### AWS EC2

```bash
# SSH into EC2 instance
ssh -i key.pem ec2-user@your-instance

# Install Python
sudo yum install python3

# Clone/upload project
# Install dependencies
pip3 install -r requirements.txt

# Run with nohup
nohup python3 app.py &
```

---

## System Requirements

### Minimum
- **CPU**: 1 GHz processor
- **RAM**: 2 GB
- **Storage**: 1 GB free space
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distro)

### Recommended
- **CPU**: 2+ GHz multi-core processor
- **RAM**: 4+ GB
- **Storage**: 2+ GB free space
- **OS**: Windows 10+, macOS 11+, Ubuntu 20.04+

---

## Getting Help

### Installation Issues
1. Check this guide first
2. Verify Python version: `python --version`
3. Check pip: `pip --version`
4. Try virtual environment method
5. Install packages individually

### Runtime Issues
1. Run test suite: `python test_app.py`
2. Check console for errors
3. Verify all files present
4. Try with sample_data.csv

---

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] pip working
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts (`python app.py`)
- [ ] Browser opens (`http://localhost:5000`)
- [ ] Sample data works (`sample_data.csv`)
- [ ] Tests pass (`python test_app.py`)

---

## Success!

If you see this in your browser:

```
🤖 AI Data Analyst
Professional Data Analysis Platform
Upload Any Dataset for Instant Insights
```

**Congratulations! Installation complete!** 🎉

You're ready to analyze data!

---

## Next Steps

1. **Read**: `USAGE_GUIDE.md` for detailed instructions
2. **Try**: Upload `sample_data.csv` to test
3. **Explore**: Check all 9 result tabs
4. **Learn**: Review generated Python/SQL/DAX code
5. **Analyze**: Upload your own datasets!

---

**Need more help?** Check `README.md` and `USAGE_GUIDE.md`

**Happy analyzing!** 📊🚀
