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
import google.generativeai as genai
import warnings
warnings.filterwarnings('ignore')

# Configure Gemini API
genai.configure(api_key='AIzaSyDj7q6p1Y4Yz4MI6COBdvGCS7CV0D-vFoE')

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

class AIDataAnalyst:
    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()
        self.column_types = {}
        
    def understand_data(self):
        """Stage 1: Data Understanding"""
        info = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'memory_usage': safe_float(self.df.memory_usage(deep=True).sum() / 1024**2),
            'head': self.df.head(10).replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict('records')
        }
        
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                if self.df[col].nunique() < 20:
                    self.column_types[col] = 'categorical_numeric'
                else:
                    self.column_types[col] = 'numerical'
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.column_types[col] = 'datetime'
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
        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing > 0:
                cleaning_report['missing_values'][col] = int(missing)
                
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    self.df[col].fillna('Unknown', inplace=True)
        
        # Duplicates
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        cleaning_report['duplicates_removed'] = before - len(self.df)
        
        # Outliers
        for col in self.df.select_dtypes(include=[np.number]).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                cleaning_report['outliers_detected'][col] = int(outliers)
        
        return cleaning_report
    
    def perform_eda(self):
        """Stage 3: EDA"""
        eda_results = {'descriptive_stats': {}, 'correlations': {}}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            eda_results['descriptive_stats'][col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max())
            }
        
        if len(numeric_cols) > 1:
            corr = self.df[numeric_cols].corr()
            eda_results['correlations'] = corr.replace({np.nan: None, np.inf: None, -np.inf: None}).to_dict()
        
        return eda_results
    
    def generate_visualizations(self):
        """Stage 4: Generate Visualizations"""
        charts = []
        sns.set_style('whitegrid')
        plt.rcParams['figure.dpi'] = 100
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Chart 1: Correlation Heatmap
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = self.df[numeric_cols[:10]].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f', ax=ax)
            ax.set_title('Correlation Matrix')
            charts.append({'title': 'Correlation Heatmap', 'image': fig_to_base64(fig)})
            plt.close()
        
        # Chart 2: Distribution plots
        if len(numeric_cols) >= 1:
            n_cols = min(3, len(numeric_cols))
            fig, axes = plt.subplots(2, n_cols, figsize=(15, 10), squeeze=False)
            
            for idx, col in enumerate(numeric_cols[:n_cols]):
                axes[0, idx].hist(self.df[col].dropna(), bins=30, edgecolor='black', color='skyblue')
                axes[0, idx].set_title(f'{col} Distribution')
                axes[1, idx].boxplot(self.df[col].dropna())
                axes[1, idx].set_title(f'{col} Outliers')
            
            plt.tight_layout()
            charts.append({'title': 'Distribution Analysis', 'image': fig_to_base64(fig)})
            plt.close()
        
        return charts
    
    def generate_insights(self):
        """Stage 5: Business Insights"""
        insights = []
        insights.append(f"Dataset contains {len(self.df):,} records and {len(self.df.columns)} columns")
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if any(kw in col.lower() for kw in ['sales', 'revenue', 'profit', 'amount']):
                total = self.df[col].sum()
                avg = self.df[col].mean()
                insights.append(f"Total {col}: {total:,.2f} | Average: {avg:,.2f}")
        
        return insights
    
    def generate_ai_insights(self):
        """Stage 6: AI Insights with Gemini"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
            
            prompt = f"""You are a SENIOR DATA ANALYST. Analyze this dataset:

DATASET OVERVIEW:
- Rows: {len(self.df):,}
- Columns: {len(self.df.columns)}
- Numeric: {', '.join(numeric_cols[:5])}
- Categorical: {', '.join(categorical_cols[:5])}

SAMPLE DATA:
{self.df.head(5).to_string()}

STATISTICS:
{self.df.describe().to_string()}

Provide:
1. KEY INSIGHTS (5 specific findings with numbers)
2. BUSINESS RECOMMENDATIONS (5 actionable steps)
3. PREDICTIVE OPPORTUNITIES (what can be predicted)
4. DATA QUALITY CONCERNS
5. STRATEGIC QUESTIONS to explore

Be specific, use numbers, make it actionable."""
            
            response = model.generate_content(prompt)
            return {
                'ai_insights': response.text,
                'generated_by': 'Google Gemini Pro',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'ai_insights': f'AI Insights unavailable: {str(e)}',
                'generated_by': 'Error'
            }

def safe_float(value, default=0.0):
    try:
        if value is None or np.isnan(value) or np.isinf(value):
            return default
        return float(value)
    except:
        return default

def fig_to_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    return img_str

def load_data(file):
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
    
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', na=False)]
    df = df.reset_index(drop=True)
    return df

@app.route('/')
def index():
    return render_template('index_final.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        df = load_data(file)
        
        analyst = AIDataAnalyst(df)
        
        result = {}
        result["understanding"] = analyst.understand_data()
        result["cleaning"] = analyst.clean_data()
        result["eda"] = analyst.perform_eda()
        result["insights"] = analyst.generate_insights()
        result["charts"] = analyst.generate_visualizations()
        result["ai_insights"] = analyst.generate_ai_insights()
        result["executive_summary"] = f"Analyzed {len(df):,} records with AI-powered insights"
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
