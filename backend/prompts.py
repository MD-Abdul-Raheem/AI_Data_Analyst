INSIGHTS_PROMPT = """You are a data analyst. Analyze this dataset profile and provide 5-7 key business insights.

Dataset Profile:
- Rows: {rows}
- Columns: {columns}
- Quality Score: {quality_score}%

Column Details:
{column_details}

Top Correlations:
{correlations}

Provide insights in this JSON format:
{{"insights": ["insight 1", "insight 2", ...]}}
"""

SQL_PROMPT = """Generate 5 useful SQL queries for this dataset.

Table name: dataset
Columns: {columns}

Return JSON:
{{"queries": [{{"name": "query name", "sql": "SELECT ..."}}, ...]}}
"""

PYTHON_PROMPT = """Generate a complete Python analysis script for this dataset.

Filename: {filename}
Columns: {columns}

Include: imports, loading, cleaning, EDA, visualizations.
Return as: {{"code": "import pandas as pd\\n..."}}
"""

DAX_PROMPT = """Generate 5-10 Power BI DAX measures for this dataset.

Columns: {columns}

Return JSON:
{{"measures": [{{"name": "Total Sales", "dax": "Total Sales = SUM('Table'[Sales])"}}, ...]}}
"""
