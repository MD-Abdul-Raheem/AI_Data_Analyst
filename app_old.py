import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, jsonify, send_file
from flask.json.provider import DefaultJSONProvider
from werkzeug.utils import secure_filename
from io import BytesIO, StringIO
import base64
from datetime import datetime
from scipy import stats

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating)):
            if np.isnan(obj) or np.isinf(obj):
                return None
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

app = Flask(__name__)
app.json = CustomJSONProvider(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DataAnalyst:
    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()
        self.insights = []
        self.charts = []
        self.column_types = {}
        
    def understand_data(self):
        """Stage 1: Data Understanding"""
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'memory_usage': float(self.df.memory_usage(deep=True).sum() / 1024**2),
            'head': self.df.head(10).replace({np.nan: None}).to_dict('records'),
            'tail': self.df.tail(10).replace({np.nan: None}).to_dict('records')
        }
        
        # Classify columns
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                if self.df[col].nunique() < 20 and self.df[col].nunique() / len(self.df) < 0.05:
                    self.column_types[col] = 'categorical_numeric'
                else:
                    self.column_types[col] = 'numerical'
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.column_types[col] = 'datetime'
            elif self.df[col].dtype == 'bool':
                self.column_types[col] = 'boolean'
            elif self.df[col].nunique() == len(self.df):
                self.column_types[col] = 'id'
            else:
                self.column_types[col] = 'categorical'
        
        info['column_types'] = self.column_types
        return info
    
    def clean_data(self):
        """Stage 2: Data Cleaning"""
        cleaning_report = {
            'missing_values': {},
            'duplicates_removed': 0,
            'outliers_detected': {},
            'transformations': []
        }
        
        # Missing values
        missing = self.df.isnull().sum()
        cleaning_report['missing_values'] = missing[missing > 0].to_dict()
        
        # Fill missing values
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.column_types.get(col) == 'numerical':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                    cleaning_report['transformations'].append(f"{col}: filled with median")
                else:
                    self.df[col].fillna('Unknown', inplace=True)
                    cleaning_report['transformations'].append(f"{col}: filled with 'Unknown'")
        
        # Remove duplicates
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        cleaning_report['duplicates_removed'] = before - len(self.df)
        
        # Standardize strings
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].astype(str).str.strip().str.title()
        
        # Detect datetime columns and convert
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.column_types[col] = 'datetime'
                    cleaning_report['transformations'].append(f"{col}: converted to datetime")
                except:
                    pass
        
        # Detect outliers
        for col in self.df.select_dtypes(include=[np.number]).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                cleaning_report['outliers_detected'][col] = int(outliers)
        
        return cleaning_report
    
    def perform_eda(self):
        """Stage 3: Exploratory Data Analysis"""
        eda_results = {
            'numerical_summary': {},
            'categorical_summary': {},
            'correlations': {},
            'distributions': {}
        }
        
        # Numerical summary
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            eda_results['numerical_summary'] = self.df[numeric_cols].describe().replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict()
            
            # Correlation matrix
            if len(numeric_cols) > 1:
                corr = self.df[numeric_cols].corr()
                eda_results['correlations'] = corr.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict()
        
        # Categorical summary
        categorical_cols = [col for col, ctype in self.column_types.items() 
                          if ctype in ['categorical', 'categorical_numeric']]
        for col in categorical_cols[:10]:
            value_counts = self.df[col].value_counts().head(20)
            eda_results['categorical_summary'][col] = value_counts.to_dict()
        
        return eda_results
    
    def generate_insights(self):
        """Stage 4: Business Insights"""
        insights = []
        
        # Dataset overview
        insights.append(f"Dataset contains {len(self.df):,} records and {len(self.df.columns)} columns")
        
        # Identify potential KPI columns
        kpi_keywords = ['sales', 'revenue', 'profit', 'amount', 'price', 'quantity', 'units', 'cost']
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            col_lower = col.lower()
            if any(kw in col_lower for kw in kpi_keywords):
                total = self.df[col].sum()
                avg = self.df[col].mean()
                insights.append(f"Total {col}: {total:,.2f} | Average: {avg:,.2f}")
        
        # Top performers
        categorical_cols = [col for col, ctype in self.column_types.items() 
                          if ctype in ['categorical', 'categorical_numeric']]
        
        for cat_col in categorical_cols[:3]:
            if self.df[cat_col].nunique() < 100:
                top_item = self.df[cat_col].value_counts().head(1)
                if len(top_item) > 0:
                    insights.append(f"Top {cat_col}: {top_item.index[0]} ({top_item.values[0]:,} occurrences)")
        
        # Datetime trends
        datetime_cols = [col for col, ctype in self.column_types.items() if ctype == 'datetime']
        if datetime_cols:
            date_col = datetime_cols[0]
            date_range = f"{self.df[date_col].min()} to {self.df[date_col].max()}"
            insights.append(f"Date range: {date_range}")
        
        # Missing data quality
        missing_pct = (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        insights.append(f"Data completeness: {100-missing_pct:.1f}%")
        
        return insights
    
    def generate_python_code(self, filename='your_data.csv'):
        """Stage 5: Python Pandas Code"""
        code = f"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
# Replace with your actual file path
df = pd.read_csv('{filename}')  # Adjust file path as needed

# Data Understanding
print("Shape:", df.shape)
print("\\nColumns:", df.columns.tolist())
print("\\nData Types:")
print(df.dtypes)
print("\\nFirst 10 rows:")
print(df.head(10))
print("\\nLast 10 rows:")
print(df.tail(10))

# Data Cleaning
print("\\nMissing Values:")
print(df.isnull().sum())

# Fill missing values
for col in df.select_dtypes(include=[np.number]).columns:
    df[col].fillna(df[col].median(), inplace=True)
for col in df.select_dtypes(include=['object']).columns:
    df[col].fillna('Unknown', inplace=True)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Standardize strings
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].str.strip().str.title()

# EDA - Numerical Summary
print("\\nNumerical Summary:")
print(df.describe())

# EDA - Categorical Summary
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    print(f"\\n{{col}} - Top 10:")
    print(df[col].value_counts().head(10))

# Correlation Matrix
numeric_df = df.select_dtypes(include=[np.number])
if len(numeric_df.columns) > 1:
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')
    plt.close()

# Visualizations
for col in numeric_df.columns[:5]:
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.hist(df[col].dropna(), bins=30, edgecolor='black')
    plt.title(f'{{col}} Distribution')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    
    plt.subplot(1, 2, 2)
    plt.boxplot(df[col].dropna())
    plt.title(f'{{col}} Boxplot')
    plt.ylabel(col)
    plt.tight_layout()
    plt.savefig(f'{{col}}_analysis.png')
    plt.close()

print("\\nAnalysis complete!")
"""
        return code
    
    def generate_sql_queries(self):
        """Stage 6: SQL Query Generation"""
        queries = []
        
        # Detect potential table name
        table_name = "dataset"
        
        queries.append({
            "name": "Top 10 Records",
            "query": f"SELECT * FROM {table_name} LIMIT 10;"
        })
        
        # Find potential grouping columns
        categorical_cols = [col for col, ctype in self.column_types.items() 
                          if ctype in ['categorical', 'categorical_numeric']]
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if categorical_cols and numeric_cols:
            group_col = categorical_cols[0]
            value_col = numeric_cols[0]
            queries.append({
                "name": f"Top 10 by {value_col}",
                "query": f"SELECT {group_col}, SUM({value_col}) as total_{value_col}\nFROM {table_name}\nGROUP BY {group_col}\nORDER BY total_{value_col} DESC\nLIMIT 10;"
            })
        
        # Date-based query
        datetime_cols = [col for col, ctype in self.column_types.items() if ctype == 'datetime']
        if datetime_cols and numeric_cols:
            date_col = datetime_cols[0]
            value_col = numeric_cols[0]
            queries.append({
                "name": "Monthly Trend",
                "query": f"SELECT DATE_TRUNC('month', {date_col}) as month,\n       SUM({value_col}) as total_{value_col}\nFROM {table_name}\nGROUP BY month\nORDER BY month;"
            })
        
        queries.append({
            "name": "Data Quality Check",
            "query": f"SELECT COUNT(*) as total_records,\n       COUNT(DISTINCT *) as unique_records\nFROM {table_name};"
        })
        
        return queries
    
    def generate_dax_measures(self):
        """Stage 7: Power BI DAX Measures"""
        measures = []
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        for col in numeric_cols[:5]:
            measures.append({
                "name": f"Total {col}",
                "dax": f"Total {col} = SUM('{col}'[{col}])"
            })
            
            measures.append({
                "name": f"Average {col}",
                "dax": f"Average {col} = AVERAGE('{col}'[{col}])"
            })
        
        measures.append({
            "name": "Total Records",
            "dax": "Total Records = COUNTROWS(Dataset)"
        })
        
        datetime_cols = [col for col, ctype in self.column_types.items() if ctype == 'datetime']
        if datetime_cols and numeric_cols:
            value_col = numeric_cols[0]
            measures.append({
                "name": f"{value_col} YoY Growth",
                "dax": f"{value_col} YoY Growth = \nVAR CurrentYear = SUM('{value_col}'[{value_col}])\nVAR PreviousYear = CALCULATE(SUM('{value_col}'[{value_col}]), SAMEPERIODLASTYEAR(Date[Date]))\nRETURN DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0)"
            })
        
        return measures
    
    def generate_json_output(self, understanding, cleaning, eda, insights, python_code, sql_queries, dax_measures):
        """Stage 8: Structured JSON Output"""
        return {
            "summary": f"Analysis of dataset with {len(self.df)} records and {len(self.df.columns)} columns",
            "columns": understanding['column_types'],
            "data_quality": {
                "missing_values": cleaning['missing_values'],
                "duplicates_removed": cleaning['duplicates_removed'],
                "outliers": cleaning['outliers_detected']
            },
            "key_insights": insights,
            "python_code": python_code,
            "sql_queries": sql_queries,
            "dax_measures": dax_measures,
            "recommended_charts": ["Correlation Heatmap", "Distribution Histograms", "Boxplots", "Bar Charts", "Time Series"],
            "business_recommendations": [
                "Focus on top performing categories",
                "Investigate outliers for anomalies",
                "Monitor trends over time",
                "Address data quality issues"
            ]
        }
    
    def generate_notebook(self, python_code):
        """Stage 9: Generate Jupyter Notebook"""
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# AI Data Analyst - Automated Analysis\n", f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "source": python_code.split('\n')
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        return notebook

def load_data(file):
    """Load data from various formats"""
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    if filename.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(filepath)
    elif filename.endswith('.json'):
        df = pd.read_json(filepath)
    else:
        raise ValueError("Unsupported file format")
    
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Load data
        if 'file' in request.files:
            file = request.files['file']
            df = load_data(file)
        elif 'raw_data' in request.form:
            raw_data = request.form['raw_data']
            df = pd.read_csv(StringIO(raw_data))
        else:
            return jsonify({"error": "No data provided"}), 400
        
        # Initialize analyst
        analyst = DataAnalyst(df)
        
        # Stage 1: Understand
        understanding = analyst.understand_data()
        
        # Stage 2: Clean
        cleaning = analyst.clean_data()
        
        # Stage 3: EDA
        eda = analyst.perform_eda()
        
        # Stage 4: Insights
        insights = analyst.generate_insights()
        
        # Stage 5: Python Code
        filename = file.filename if 'file' in request.files else 'your_data.csv'
        python_code = analyst.generate_python_code(filename)
        
        # Stage 6: SQL
        sql_queries = analyst.generate_sql_queries()
        
        # Stage 7: DAX
        dax_measures = analyst.generate_dax_measures()
        
        # Stage 8: JSON
        json_output = analyst.generate_json_output(
            understanding, cleaning, eda, insights, 
            python_code, sql_queries, dax_measures
        )
        
        # Stage 9: Notebook
        notebook = analyst.generate_notebook(python_code)
        
        # Stage 10: Final deliverables
        result = {
            "understanding": understanding,
            "cleaning": cleaning,
            "eda": eda,
            "insights": insights,
            "python_code": python_code,
            "sql_queries": sql_queries,
            "dax_measures": dax_measures,
            "json_output": json_output,
            "notebook": notebook,
            "executive_summary": f"Analyzed {len(df):,} records across {len(df.columns)} dimensions. Cleaned {cleaning['duplicates_removed']} duplicates. Generated {len(insights)} key insights."
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/notebook', methods=['POST'])
def download_notebook():
    notebook_data = request.json.get('notebook')
    buffer = BytesIO()
    buffer.write(json.dumps(notebook_data, indent=2).encode())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='analysis.ipynb', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
