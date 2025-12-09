# ⚡ AI Data Analyst - Quick Reference Card

## 🚀 Start Application

```bash
# Method 1: Python
python app.py

# Method 2: Batch file (Windows)
run.bat

# Then open: http://localhost:5000
```

---

## 📊 10-Stage Analysis Pipeline

| Stage | What It Does | Output |
|-------|-------------|--------|
| 1️⃣ **Data Understanding** | Reads dataset, identifies columns | Metadata, preview |
| 2️⃣ **Data Cleaning** | Fixes missing values, removes duplicates | Cleaned data, report |
| 3️⃣ **EDA** | Statistical analysis, distributions | Summaries, correlations |
| 4️⃣ **Business Insights** | Detects KPIs, top performers | Insight bullets |
| 5️⃣ **Python Code** | Generates Pandas script | .py file |
| 6️⃣ **SQL Queries** | Creates database queries | SQL statements |
| 7️⃣ **DAX Measures** | Power BI calculations | DAX formulas |
| 8️⃣ **JSON Output** | Structured results | JSON file |
| 9️⃣ **Notebook** | Jupyter notebook | .ipynb file |
| 🔟 **Deliverables** | Packages everything | Complete report |

---

## 📁 Supported File Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| CSV | `.csv` | Fastest processing |
| Excel | `.xlsx`, `.xls` | All sheets supported |
| JSON | `.json` | Nested structures OK |
| Raw Data | Paste directly | CSV format |

---

## 🎯 Column Type Detection

| Type | Description | Example |
|------|-------------|---------|
| **numerical** | Numbers for calculations | Sales: 1234.56 |
| **categorical** | Text categories | Product: "Laptop" |
| **datetime** | Dates and times | Date: 2024-01-15 |
| **boolean** | True/False | Active: True |
| **id** | Unique identifiers | Order_ID: 1001 |

---

## 🧹 Automatic Cleaning

| Issue | Solution |
|-------|----------|
| Missing numbers | Fill with median |
| Missing text | Fill with "Unknown" |
| Duplicates | Remove automatically |
| Messy strings | Trim & standardize |
| Wrong types | Auto-convert |
| Outliers | Flag (not remove) |

---

## 📈 Generated Outputs

### Python Code
```python
import pandas as pd
import numpy as np
# Complete analysis script
# Ready to run
```

### SQL Queries
```sql
SELECT Product, SUM(Sales)
FROM dataset
GROUP BY Product
ORDER BY SUM(Sales) DESC;
```

### Power BI DAX
```dax
Total Sales = SUM('Sales'[Amount])
YoY Growth = [Current] - [Previous]
```

---

## 🔧 API Quick Reference

### Analyze File
```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@data.csv"
```

### Analyze Raw Data
```bash
curl -X POST http://localhost:5000/analyze \
  -d "raw_data=Name,Age\nJohn,30"
```

### Python Client
```python
import requests

with open('data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/analyze',
        files={'file': f}
    )
result = response.json()
```

---

## 📊 UI Tabs Overview

| Tab | Content |
|-----|---------|
| 📋 **Executive Summary** | Overview, metrics, key numbers |
| 💡 **Business Insights** | Actionable insights, KPIs |
| 📊 **Data Overview** | Column types, preview |
| 🧹 **Data Cleaning** | Quality report, fixes |
| 📈 **EDA Results** | Statistics, distributions |
| 🐍 **Python Code** | Complete script |
| 💾 **SQL Queries** | Database queries |
| 📊 **Power BI DAX** | BI measures |
| 📄 **JSON Output** | Structured data |

---

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Upload file | Click upload box |
| Paste data | Click "Paste Raw Data" |
| Switch tabs | Click tab buttons |
| Download | Click download buttons |

---

## 🎯 Common Use Cases

### Sales Analysis
1. Upload sales CSV
2. Check Business Insights
3. Copy SQL queries
4. Use DAX in Power BI

### Data Quality Check
1. Upload dataset
2. Go to Data Cleaning tab
3. Review missing values
4. Check outliers

### Quick Report
1. Upload data
2. Screenshot Executive Summary
3. Copy insights
4. Share with team

---

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | `pip install -r requirements.txt` |
| Analysis fails | Check file format |
| Slow performance | Reduce file size |
| No insights | Ensure numerical columns exist |
| Upload error | Verify file < 100MB |

---

## 📦 Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run application
python app.py

# 3. Open browser
http://localhost:5000

# 4. Upload data
# 5. Get insights!
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Quick start guide |
| `USAGE_GUIDE.md` | Complete manual |
| `API_DOCUMENTATION.md` | API reference |
| `PROJECT_OVERVIEW.md` | Full project details |
| `QUICK_REFERENCE.md` | This file |

---

## 🎨 Key Features

✅ **Zero Configuration** - Just upload and analyze
✅ **10-Stage Pipeline** - Complete workflow
✅ **Multi-Format** - CSV, Excel, JSON
✅ **Code Generation** - Python, SQL, DAX
✅ **Business Insights** - Automatic KPI detection
✅ **Data Cleaning** - Automatic fixes
✅ **Professional Output** - Production-ready
✅ **Fast** - Seconds, not hours

---

## 📊 Example Insights

```
✓ Dataset contains 1,000 records and 10 columns
✓ Total Sales: $45,234.50 | Average: $1,508.12
✓ Top Product: Laptop (15 occurrences)
✓ Date range: 2024-01-15 to 2024-02-14
✓ Data completeness: 98.5%
```

---

## 🔗 Quick Links

- **Start Server**: `python app.py`
- **Run Tests**: `python test_app.py`
- **Sample Data**: `sample_data.csv`
- **Web Interface**: `http://localhost:5000`

---

## 💡 Pro Tips

1. **Use CSV** for fastest processing
2. **Clean column names** before upload
3. **Start with sample data** to test
4. **Review all tabs** for complete picture
5. **Customize generated code** for your needs
6. **Download deliverables** for offline use

---

## 📞 Need Help?

1. Check `USAGE_GUIDE.md` for detailed help
2. Review error messages in console
3. Test with `sample_data.csv`
4. Run `test_app.py` to verify setup

---

## 🎯 Performance Guide

| Dataset Size | Processing Time |
|--------------|-----------------|
| < 1K rows | 1-3 seconds |
| 1K-10K rows | 3-10 seconds |
| 10K-100K rows | 10-30 seconds |
| > 100K rows | 30+ seconds |

---

## 🚀 Getting Started (30 seconds)

```bash
# 1. Install (one time)
pip install -r requirements.txt

# 2. Start
python app.py

# 3. Upload
# Open http://localhost:5000
# Drag & drop your CSV file

# 4. Analyze
# Wait 5-10 seconds

# 5. Explore
# Click through 9 result tabs

# 6. Download
# Get Python code, SQL, DAX, Notebook
```

---

**That's it! You're ready to analyze any dataset! 🎉**

---

## 📋 Checklist

Before first use:
- [ ] Python installed (3.8+)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python app.py`)
- [ ] Browser open (`http://localhost:5000`)
- [ ] Test file ready (use `sample_data.csv`)

---

## 🎓 What You Get

Every analysis includes:

1. ✅ **Executive Summary** - High-level overview
2. ✅ **Business Insights** - Actionable findings
3. ✅ **Data Quality Report** - Cleaning details
4. ✅ **Statistical Analysis** - EDA results
5. ✅ **Python Code** - Reproducible script
6. ✅ **SQL Queries** - Database ready
7. ✅ **DAX Measures** - Power BI ready
8. ✅ **JSON Report** - API ready
9. ✅ **Jupyter Notebook** - Interactive analysis

---

**Print this page for quick reference! 📄**

Transform any dataset into insights in seconds! 🚀
