# 🔌 AI Data Analyst - API Documentation

## Overview

The AI Data Analyst provides a RESTful API for programmatic access to data analysis capabilities.

---

## Base URL

```
http://localhost:5000
```

---

## Endpoints

### 1. Home Page

**Endpoint:** `GET /`

**Description:** Returns the main web interface

**Response:** HTML page

---

### 2. Analyze Data

**Endpoint:** `POST /analyze`

**Description:** Performs complete data analysis on uploaded file or raw data

**Content-Type:** `multipart/form-data` or `application/x-www-form-urlencoded`

#### Request Parameters

**Option A: File Upload**
```
file: File (CSV, Excel, or JSON)
```

**Option B: Raw Data**
```
raw_data: String (CSV formatted text)
```

#### Example Request (cURL - File Upload)

```bash
curl -X POST http://localhost:5000/analyze \
  -F "file=@sales_data.csv"
```

#### Example Request (cURL - Raw Data)

```bash
curl -X POST http://localhost:5000/analyze \
  -d "raw_data=Name,Age,City
John,30,NYC
Jane,25,LA"
```

#### Example Request (Python)

```python
import requests

# File upload
with open('sales_data.csv', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/analyze',
        files={'file': f}
    )

# Raw data
response = requests.post(
    'http://localhost:5000/analyze',
    data={'raw_data': 'Name,Age\nJohn,30\nJane,25'}
)

result = response.json()
print(result['insights'])
```

#### Example Request (JavaScript)

```javascript
// File upload
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/analyze', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));

// Raw data
const formData = new FormData();
formData.append('raw_data', 'Name,Age\nJohn,30\nJane,25');

fetch('http://localhost:5000/analyze', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

#### Response Schema

```json
{
  "understanding": {
    "shape": [30, 10],
    "columns": ["Order_ID", "Date", "Product", ...],
    "dtypes": {"Order_ID": "int64", "Date": "object", ...},
    "memory_usage": 2.34,
    "head": [{...}, {...}],
    "tail": [{...}, {...}],
    "column_types": {
      "Order_ID": "id",
      "Date": "datetime",
      "Product": "categorical",
      "Sales": "numerical"
    }
  },
  "cleaning": {
    "missing_values": {"Column1": 5, "Column2": 3},
    "duplicates_removed": 2,
    "outliers_detected": {"Sales": 3, "Profit": 1},
    "transformations": [
      "Sales: filled with median",
      "Date: converted to datetime"
    ]
  },
  "eda": {
    "numerical_summary": {
      "Sales": {
        "count": 30,
        "mean": 1234.56,
        "std": 456.78,
        "min": 100.00,
        "25%": 500.00,
        "50%": 1000.00,
        "75%": 1500.00,
        "max": 5000.00
      }
    },
    "categorical_summary": {
      "Product": {
        "Laptop": 10,
        "Mouse": 8,
        "Keyboard": 7
      }
    },
    "correlations": {
      "Sales": {"Sales": 1.0, "Profit": 0.85},
      "Profit": {"Sales": 0.85, "Profit": 1.0}
    }
  },
  "insights": [
    "Dataset contains 30 records and 10 columns",
    "Total Sales: 37,036.70 | Average: 1,234.56",
    "Top Product: Laptop (10 occurrences)",
    "Date range: 2024-01-15 to 2024-02-14",
    "Data completeness: 98.5%"
  ],
  "python_code": "import pandas as pd\nimport numpy as np\n...",
  "sql_queries": [
    {
      "name": "Top 10 Records",
      "query": "SELECT * FROM dataset LIMIT 10;"
    },
    {
      "name": "Top 10 by Sales",
      "query": "SELECT Product, SUM(Sales) as total_sales\nFROM dataset\nGROUP BY Product\nORDER BY total_sales DESC\nLIMIT 10;"
    }
  ],
  "dax_measures": [
    {
      "name": "Total Sales",
      "dax": "Total Sales = SUM('Sales'[Sales])"
    },
    {
      "name": "Average Sales",
      "dax": "Average Sales = AVERAGE('Sales'[Sales])"
    }
  ],
  "json_output": {
    "summary": "Analysis of dataset with 30 records and 10 columns",
    "columns": {...},
    "data_quality": {...},
    "key_insights": [...],
    "python_code": "...",
    "sql_queries": [...],
    "dax_measures": [...],
    "recommended_charts": [...],
    "business_recommendations": [...]
  },
  "notebook": {
    "cells": [...],
    "metadata": {...},
    "nbformat": 4,
    "nbformat_minor": 4
  },
  "executive_summary": "Analyzed 30 records across 10 dimensions. Cleaned 2 duplicates. Generated 5 key insights."
}
```

#### Error Response

```json
{
  "error": "Error message describing what went wrong"
}
```

**Status Codes:**
- `200 OK`: Analysis completed successfully
- `400 Bad Request`: No data provided or invalid format
- `500 Internal Server Error`: Server error during analysis

---

### 3. Download Notebook

**Endpoint:** `POST /download/notebook`

**Description:** Downloads the generated Jupyter notebook

**Content-Type:** `application/json`

#### Request Body

```json
{
  "notebook": {
    "cells": [...],
    "metadata": {...},
    "nbformat": 4,
    "nbformat_minor": 4
  }
}
```

#### Example Request (Python)

```python
import requests

notebook_data = analysis_result['notebook']

response = requests.post(
    'http://localhost:5000/download/notebook',
    json={'notebook': notebook_data}
)

with open('analysis.ipynb', 'wb') as f:
    f.write(response.content)
```

#### Response

Binary file download (`.ipynb` format)

---

## Data Models

### Column Types

The system automatically classifies columns into these types:

- **numerical**: Numeric data for calculations (int, float)
- **categorical**: Text categories with limited unique values
- **categorical_numeric**: Numbers used as categories (ratings, IDs)
- **datetime**: Date and time values
- **boolean**: True/False values
- **id**: Unique identifiers

### Cleaning Operations

Automatic cleaning includes:

1. **Missing Values:**
   - Numerical: Filled with median
   - Categorical: Filled with "Unknown"

2. **Duplicates:**
   - Exact duplicate rows removed

3. **Standardization:**
   - Strings trimmed and title-cased
   - Dates converted to datetime format

4. **Outlier Detection:**
   - IQR method (1.5 × Interquartile Range)
   - Flagged but not removed

---

## Integration Examples

### Python Integration

```python
import requests
import pandas as pd

class DataAnalystClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
    
    def analyze_file(self, filepath):
        """Analyze a file"""
        with open(filepath, 'rb') as f:
            response = requests.post(
                f'{self.base_url}/analyze',
                files={'file': f}
            )
        return response.json()
    
    def analyze_dataframe(self, df):
        """Analyze a pandas DataFrame"""
        csv_data = df.to_csv(index=False)
        response = requests.post(
            f'{self.base_url}/analyze',
            data={'raw_data': csv_data}
        )
        return response.json()
    
    def get_insights(self, filepath):
        """Get just the insights"""
        result = self.analyze_file(filepath)
        return result['insights']
    
    def get_python_code(self, filepath):
        """Get generated Python code"""
        result = self.analyze_file(filepath)
        return result['python_code']
    
    def get_sql_queries(self, filepath):
        """Get generated SQL queries"""
        result = self.analyze_file(filepath)
        return result['sql_queries']

# Usage
client = DataAnalystClient()

# Analyze file
result = client.analyze_file('sales_data.csv')
print(result['executive_summary'])

# Analyze DataFrame
df = pd.read_csv('data.csv')
result = client.analyze_dataframe(df)
for insight in result['insights']:
    print(f"✓ {insight}")

# Get specific outputs
insights = client.get_insights('sales_data.csv')
python_code = client.get_python_code('sales_data.csv')
sql_queries = client.get_sql_queries('sales_data.csv')
```

### Node.js Integration

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class DataAnalystClient {
    constructor(baseURL = 'http://localhost:5000') {
        this.baseURL = baseURL;
    }
    
    async analyzeFile(filepath) {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(filepath));
        
        const response = await axios.post(
            `${this.baseURL}/analyze`,
            formData,
            { headers: formData.getHeaders() }
        );
        
        return response.data;
    }
    
    async analyzeRawData(csvData) {
        const formData = new FormData();
        formData.append('raw_data', csvData);
        
        const response = await axios.post(
            `${this.baseURL}/analyze`,
            formData,
            { headers: formData.getHeaders() }
        );
        
        return response.data;
    }
    
    async getInsights(filepath) {
        const result = await this.analyzeFile(filepath);
        return result.insights;
    }
}

// Usage
const client = new DataAnalystClient();

client.analyzeFile('sales_data.csv')
    .then(result => {
        console.log(result.executive_summary);
        result.insights.forEach(insight => {
            console.log(`✓ ${insight}`);
        });
    })
    .catch(error => console.error(error));
```

### R Integration

```r
library(httr)
library(jsonlite)

analyze_file <- function(filepath, base_url = "http://localhost:5000") {
  response <- POST(
    paste0(base_url, "/analyze"),
    body = list(file = upload_file(filepath)),
    encode = "multipart"
  )
  
  content(response, "parsed")
}

analyze_dataframe <- function(df, base_url = "http://localhost:5000") {
  csv_data <- paste(capture.output(write.csv(df, row.names = FALSE)), collapse = "\n")
  
  response <- POST(
    paste0(base_url, "/analyze"),
    body = list(raw_data = csv_data),
    encode = "form"
  )
  
  content(response, "parsed")
}

# Usage
result <- analyze_file("sales_data.csv")
print(result$executive_summary)

for (insight in result$insights) {
  cat("✓", insight, "\n")
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider:

- Implementing rate limiting per IP
- Adding authentication
- Setting request quotas
- Monitoring resource usage

---

## Best Practices

### File Upload
- Keep files under 100MB
- Use CSV for fastest processing
- Ensure proper encoding (UTF-8)
- Include headers in first row

### Raw Data
- Use proper CSV format
- Include column headers
- Escape special characters
- Use consistent delimiters

### Error Handling
```python
try:
    result = client.analyze_file('data.csv')
    if 'error' in result:
        print(f"Analysis error: {result['error']}")
    else:
        print(f"Success: {result['executive_summary']}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
```

---

## Security Considerations

### For Production Deployment

1. **Authentication:**
   - Implement API keys
   - Use OAuth 2.0
   - Add user authentication

2. **Input Validation:**
   - Validate file types
   - Check file sizes
   - Sanitize inputs

3. **Rate Limiting:**
   - Limit requests per user
   - Implement quotas
   - Add throttling

4. **HTTPS:**
   - Use SSL/TLS
   - Secure data transmission
   - Protect sensitive data

5. **File Storage:**
   - Clean up uploaded files
   - Use temporary storage
   - Implement file retention policies

---

## Support

For API issues or questions:
- Check error messages in response
- Verify request format
- Test with sample data
- Review this documentation

---

**API Version:** 1.0  
**Last Updated:** 2024

Happy integrating! 🚀
