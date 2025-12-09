# 📘 AI Data Analyst - Complete Usage Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the Analysis](#understanding-the-analysis)
3. [Interpreting Results](#interpreting-results)
4. [Using Generated Code](#using-generated-code)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Step 1: Installation

```bash
# Navigate to project directory
cd "AI Data Analyst VS code"

# Install required packages
pip install -r requirements.txt
```

### Step 2: Launch Application

```bash
python app.py
```

Open browser to: `http://localhost:5000`

### Step 3: Upload Data

**Option A: File Upload**
- Click the upload box
- Select CSV, Excel, or JSON file
- Wait for automatic analysis

**Option B: Paste Raw Data**
- Click "Paste Raw Data" button
- Paste CSV content
- Click "Analyze Raw Data"

---

## Understanding the Analysis

### 📋 Executive Summary Tab
**What you see:**
- Total records and columns
- Memory usage
- Quick metrics

**What it means:**
- Dataset size and complexity
- Resource requirements
- Overall data health

**Example:**
```
Analyzed 1,000 records across 10 dimensions
Cleaned 5 duplicates
Generated 8 key insights
```

### 💡 Business Insights Tab
**What you see:**
- Bullet-point insights
- KPI summaries
- Top performers
- Date ranges

**What it means:**
- Actionable business intelligence
- Key performance indicators
- Important patterns
- Data coverage

**Example Insights:**
```
✓ Total Sales: $45,234.50 | Average: $1,508.12
✓ Top Product: Laptop (15 occurrences)
✓ Date range: 2024-01-15 to 2024-02-14
✓ Data completeness: 98.5%
```

### 📊 Data Overview Tab
**What you see:**
- Column types classification
- First 10 rows preview
- Data structure

**What it means:**
- How the system interpreted your data
- Column classifications:
  - `numerical`: Numbers for calculations
  - `categorical`: Groups/categories
  - `datetime`: Date/time fields
  - `id`: Unique identifiers
  - `boolean`: True/False values

### 🧹 Data Cleaning Tab
**What you see:**
- Duplicates removed count
- Missing values by column
- Outliers detected

**What it means:**
- Data quality issues found
- Automatic fixes applied
- Potential anomalies

**Cleaning Actions Taken:**
- Missing numerical values → filled with median
- Missing categorical values → filled with "Unknown"
- Duplicates → removed
- Strings → trimmed and standardized
- Outliers → flagged (not removed)

### 📈 EDA Results Tab
**What you see:**
- Statistical summaries (mean, std, min, max)
- Top values for categories
- Correlation data

**What it means:**
- Distribution of your data
- Relationships between variables
- Most common values

### 🐍 Python Code Tab
**What you see:**
- Complete Python script
- Ready to run

**What it means:**
- Reproducible analysis
- Can be customized
- Runs independently

**How to use:**
1. Copy the code
2. Save as `analysis.py`
3. Update file path: `df = pd.read_csv('your_data.csv')`
4. Run: `python analysis.py`

### 💾 SQL Queries Tab
**What you see:**
- Multiple SQL queries
- Business intelligence queries

**What it means:**
- Database-ready queries
- Works on MySQL, PostgreSQL, BigQuery
- Can be used in BI tools

**How to use:**
1. Copy desired query
2. Replace table name if needed
3. Run in your database client
4. Use for reporting/dashboards

**Example Query:**
```sql
SELECT Product, SUM(Sales) as total_sales
FROM dataset
GROUP BY Product
ORDER BY total_sales DESC
LIMIT 10;
```

### 📊 Power BI DAX Tab
**What you see:**
- DAX measure formulas
- KPI calculations

**What it means:**
- Ready for Power BI
- Professional metrics
- Dashboard-ready

**How to use:**
1. Open Power BI Desktop
2. Go to Modeling → New Measure
3. Paste DAX code
4. Use in visualizations

**Example DAX:**
```dax
Total Sales = SUM('Sales'[Sales])
Average Sales = AVERAGE('Sales'[Sales])
```

### 📄 JSON Output Tab
**What you see:**
- Structured JSON data
- Complete analysis results

**What it means:**
- Machine-readable format
- API integration ready
- Programmatic access

**How to use:**
- Integrate with other systems
- Feed into dashboards
- Store as metadata

---

## Interpreting Results

### Understanding KPIs

**Total Sales/Revenue:**
- Sum of all sales transactions
- Indicates business volume

**Average Order Value:**
- Mean transaction size
- Shows customer spending patterns

**Top Performers:**
- Highest volume items/categories
- Focus areas for business

### Understanding Outliers

**What are outliers?**
- Data points significantly different from others
- Detected using IQR method (1.5 × Interquartile Range)

**What to do:**
- Investigate if they're errors or genuine
- Don't automatically remove them
- May represent important events

### Understanding Correlations

**Correlation values:**
- +1.0: Perfect positive correlation
- 0.0: No correlation
- -1.0: Perfect negative correlation

**Example:**
- Sales & Quantity: +0.85 (strong positive)
  → More quantity = more sales (expected)

---

## Using Generated Code

### Python Code Workflow

```python
# 1. Save the generated code
# 2. Install dependencies
pip install pandas numpy matplotlib seaborn

# 3. Update file path
df = pd.read_csv('your_actual_file.csv')

# 4. Run the script
python analysis.py

# 5. Check outputs
# - Console: Statistical summaries
# - Files: Generated charts (PNG)
```

### SQL Query Workflow

```sql
-- 1. Connect to your database
-- 2. Create/import your table
-- 3. Replace 'dataset' with your table name
-- 4. Run the query
-- 5. Export results or create views
```

### DAX Measure Workflow

```
1. Open Power BI Desktop
2. Load your data
3. Go to "Modeling" tab
4. Click "New Measure"
5. Paste DAX code
6. Adjust table/column names if needed
7. Use in visualizations
```

---

## Best Practices

### Data Preparation

✅ **DO:**
- Use clean column names (no special characters)
- Include headers in first row
- Use consistent date formats
- Remove completely empty rows/columns

❌ **DON'T:**
- Mix data types in same column
- Use merged cells (Excel)
- Include summary rows in data
- Use special characters in column names

### File Size Recommendations

- **Optimal:** < 10 MB (instant analysis)
- **Good:** 10-50 MB (few seconds)
- **Large:** 50-100 MB (may take time)
- **Very Large:** > 100 MB (consider sampling)

### Column Naming

**Good Examples:**
- `Sales`, `Revenue`, `Order_Date`
- `Customer_ID`, `Product_Name`
- `Quantity_Sold`, `Profit_Margin`

**Avoid:**
- `Sales ($)`, `Date/Time`, `Product#`
- Spaces: `Customer Name` → `Customer_Name`
- Special chars: `Profit%` → `Profit_Percent`

---

## Troubleshooting

### Common Issues

**Issue: "Error analyzing file"**
- **Solution:** Check file format (CSV, Excel, JSON only)
- Verify file isn't corrupted
- Try opening in Excel/text editor first

**Issue: "No data provided"**
- **Solution:** Ensure file is selected or data is pasted
- Check file isn't empty
- Verify CSV has proper formatting

**Issue: Missing insights**
- **Solution:** Dataset may be too small
- Ensure numerical columns exist
- Check for proper data types

**Issue: Slow analysis**
- **Solution:** Large dataset (normal)
- Close other applications
- Consider sampling data first

### Data Quality Issues

**Problem: All columns show as 'object' type**
- **Cause:** Numbers stored as text
- **Fix:** Remove currency symbols, commas
- Clean in Excel before upload

**Problem: Dates not recognized**
- **Cause:** Inconsistent date format
- **Fix:** Use standard format: YYYY-MM-DD
- Or: MM/DD/YYYY consistently

**Problem: Too many outliers**
- **Cause:** Data entry errors or genuine variance
- **Action:** Review flagged values manually
- Decide if they're valid or errors

### Performance Tips

1. **For large files:**
   - Sample first 10,000 rows
   - Analyze sample
   - Apply insights to full dataset

2. **For slow uploads:**
   - Check internet connection
   - Reduce file size
   - Remove unnecessary columns

3. **For memory errors:**
   - Close other applications
   - Restart browser
   - Use smaller dataset

---

## Advanced Usage

### Customizing Python Code

```python
# Generated code is a starting point
# Customize as needed:

# Add custom calculations
df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

# Filter data
high_value = df[df['Sales'] > 1000]

# Create custom visualizations
plt.figure(figsize=(12, 6))
df.groupby('Category')['Sales'].sum().plot(kind='bar')
plt.title('Sales by Category')
plt.savefig('custom_chart.png')
```

### Integrating SQL Queries

```sql
-- Use generated queries as templates
-- Combine multiple queries:

WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', Date) as month,
           SUM(Sales) as total_sales
    FROM dataset
    GROUP BY month
)
SELECT month, 
       total_sales,
       LAG(total_sales) OVER (ORDER BY month) as prev_month,
       total_sales - LAG(total_sales) OVER (ORDER BY month) as growth
FROM monthly_sales;
```

### Extending DAX Measures

```dax
// Build on generated measures
// Create calculated columns:

Profit Margin % = 
DIVIDE(
    [Total Profit],
    [Total Sales],
    0
) * 100

// Create measure groups:
Sales YTD = 
TOTALYTD(
    [Total Sales],
    'Date'[Date]
)
```

---

## Example Workflows

### Workflow 1: Sales Analysis

1. Upload sales data (CSV)
2. Review Executive Summary for totals
3. Check Business Insights for top products
4. Copy SQL queries for database reporting
5. Use DAX measures in Power BI dashboard
6. Download Python code for automation

### Workflow 2: Data Quality Check

1. Upload dataset
2. Go to Data Cleaning tab
3. Review missing values
4. Check outliers
5. Download cleaned data insights
6. Use Python code to replicate cleaning

### Workflow 3: Quick Reporting

1. Upload data
2. Screenshot Executive Summary
3. Copy Business Insights
4. Paste into report/presentation
5. Add context and recommendations
6. Share with stakeholders

---

## Support & Resources

### Getting Help

1. Check this guide first
2. Review error messages carefully
3. Verify data format
4. Try sample_data.csv to test

### Learning Resources

- **Pandas:** pandas.pydata.org
- **SQL:** w3schools.com/sql
- **DAX:** dax.guide
- **Power BI:** docs.microsoft.com/power-bi

### Best Practices Summary

✅ Clean data before upload
✅ Use descriptive column names
✅ Start with sample data
✅ Review all tabs
✅ Customize generated code
✅ Validate insights manually
✅ Document your findings

---

**Happy Analyzing! 📊🚀**

Transform your data into insights in seconds!
