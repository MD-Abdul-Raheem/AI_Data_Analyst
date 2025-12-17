import os
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from io import BytesIO, StringIO
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except:
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Load data
        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath, encoding='utf-8', on_bad_lines='skip')
            elif filename.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(filepath)
            else:
                return jsonify({"error": "Unsupported file format"}), 400
        elif 'raw_data' in request.form:
            df = pd.read_csv(StringIO(request.form['raw_data']))
        else:
            return jsonify({"error": "No data provided"}), 400
        
        # Basic analysis
        result = {
            "understanding": {
                "shape": list(df.shape),
                "columns": list(df.columns),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "memory_usage": float(df.memory_usage(deep=True).sum() / 1024**2),
                "head": df.head(10).fillna('').to_dict('records')
            },
            "cleaning": {
                "missing_values": df.isnull().sum().to_dict(),
                "duplicates_removed": 0
            },
            "eda": {
                "numerical_summary": df.describe().fillna(0).to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {}
            },
            "insights": [
                f"Dataset contains {len(df):,} records and {len(df.columns)} columns"
            ],
            "charts": [],
            "python_code": f"import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.head())",
            "sql_queries": [{"name": "Select All", "query": "SELECT * FROM dataset LIMIT 10;"}],
            "dax_measures": [{"name": "Total Records", "dax": "Total Records = COUNTROWS(Dataset)"}],
            "json_output": {"summary": "Analysis complete"},
            "notebook": {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 4},
            "executive_summary": f"Analyzed {len(df):,} records across {len(df.columns)} columns"
        }
        
        # Generate simple chart
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                fig, ax = plt.subplots(figsize=(10, 6))
                df[numeric_cols[0]].hist(bins=30, ax=ax)
                ax.set_title(f'Distribution of {numeric_cols[0]}')
                
                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight')
                buffer.seek(0)
                img_str = base64.b64encode(buffer.read()).decode()
                plt.close()
                
                result["charts"].append({
                    "title": f"Distribution of {numeric_cols[0]}",
                    "image": img_str,
                    "explanation": "Histogram showing data distribution"
                })
        except:
            pass
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
