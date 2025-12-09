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
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, classification_report, confusion_matrix
import statsmodels.api as sm
from statsmodels.formula.api import ols
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

class EnhancedDataAnalyst:
    def __init__(self, df):
        self.df = df
        self.original_df = df.copy()
        self.column_types = {}
        
    def understand_data(self):
        """Stage 1: Enhanced Data Understanding"""
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
        """Stage 2: Enhanced Data Cleaning"""
        cleaning_report = {
            'missing_values': {},
            'duplicates_removed': 0,
            'outliers_detected': {'iqr_method': {}, 'z_score_method': {}},
            'transformations': []
        }
        
        # Missing values
        for col in self.df.columns:
            missing = self.df[col].isnull().sum()
            if missing > 0:
                missing_pct = (missing / len(self.df)) * 100
                cleaning_report['missing_values'][col] = {'count': int(missing), 'percentage': f"{missing_pct:.2f}%"}
                
                if self.df[col].dtype in ['int64', 'float64']:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    self.df[col].fillna('Unknown', inplace=True)
        
        # Duplicates
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        cleaning_report['duplicates_removed'] = before - len(self.df)
        
        # Outliers - IQR
        for col in self.df.select_dtypes(include=[np.number]).columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                cleaning_report['outliers_detected']['iqr_method'][col] = int(outliers)
        
        # Outliers - Z-score
        for col in self.df.select_dtypes(include=[np.number]).columns:
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            outliers = (z_scores > 3).sum()
            if outliers > 0:
                cleaning_report['outliers_detected']['z_score_method'][col] = int(outliers)
        
        return cleaning_report
    
    def perform_eda(self):
        """Stage 3: Enhanced EDA"""
        eda_results = {'descriptive_stats': {}, 'correlations': {}}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            eda_results['descriptive_stats'][col] = {
                'mean': float(self.df[col].mean()),
                'median': float(self.df[col].median()),
                'std': float(self.df[col].std()),
                'variance': float(self.df[col].var()),
                'skewness': float(self.df[col].skew()),
                'kurtosis': float(self.df[col].kurtosis()),
                'min': float(self.df[col].min()),
                'max': float(self.df[col].max()),
                'q1': float(self.df[col].quantile(0.25)),
                'q3': float(self.df[col].quantile(0.75))
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
        
        # Correlation Heatmap
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            corr = self.df[numeric_cols[:10]].corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f', ax=ax)
            ax.set_title('Correlation Matrix')
            charts.append({'title': 'Correlation Heatmap', 'image': fig_to_base64(fig)})
            plt.close()
        
        # Distribution plots
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
    
    def generate_excel_formulas(self):
        """Stage 11: Excel Formulas - NEW"""
        formulas = {'aggregation': [], 'conditional': [], 'lookup': [], 'text': [], 'pivot': []}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        for col in numeric_cols[:3]:
            formulas['aggregation'].extend([
                {'function': 'SUM', 'formula': f'=SUM({col}2:{col}1000)', 'use': f'Total {col}'},
                {'function': 'AVERAGE', 'formula': f'=AVERAGE({col}2:{col}1000)', 'use': f'Average {col}'},
                {'function': 'COUNT', 'formula': f'=COUNT({col}2:{col}1000)', 'use': f'Count {col}'}
            ])
        
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            avg = self.df[col].mean()
            formulas['conditional'].extend([
                {'function': 'IF', 'formula': f'=IF({col}2>{avg:.2f},"High","Low")', 'use': 'Categorize values'},
                {'function': 'COUNTIF', 'formula': f'=COUNTIF({col}2:{col}1000,">{avg:.2f}")', 'use': 'Count above average'}
            ])
        
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            formulas['lookup'].append({
                'function': 'VLOOKUP',
                'formula': f'=VLOOKUP(lookup_value, A:B, 2, FALSE)',
                'use': 'Find matching values'
            })
        
        for col in categorical_cols[:2]:
            formulas['text'].extend([
                {'function': 'UPPER', 'formula': f'=UPPER({col}2)', 'use': 'Convert to uppercase'},
                {'function': 'TRIM', 'formula': f'=TRIM({col}2)', 'use': 'Remove extra spaces'}
            ])
        
        formulas['pivot'] = [{
            'rows': categorical_cols[0] if len(categorical_cols) > 0 else 'Category',
            'values': f'Sum of {numeric_cols[0]}' if len(numeric_cols) > 0 else 'Count',
            'purpose': 'Performance summary'
        }]
        
        return formulas
    
    def perform_advanced_statistics(self):
        """Stage 12: Advanced Statistics - NEW"""
        stats_results = {'normality_tests': {}, 'correlation_tests': {}, 'confidence_intervals': {}}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # Normality tests
        for col in numeric_cols:
            data = self.df[col].dropna()
            if len(data) > 3:
                shapiro_stat, shapiro_p = stats.shapiro(data[:5000])
                stats_results['normality_tests'][col] = {
                    'shapiro_statistic': float(shapiro_stat),
                    'p_value': float(shapiro_p),
                    'is_normal': shapiro_p > 0.05,
                    'interpretation': 'Normal' if shapiro_p > 0.05 else 'Not Normal'
                }
        
        # Correlation significance
        if len(numeric_cols) >= 2:
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    data1 = self.df[col1].dropna()
                    data2 = self.df[col2].dropna()
                    common_idx = data1.index.intersection(data2.index)
                    if len(common_idx) > 2:
                        pearson_r, pearson_p = stats.pearsonr(data1[common_idx], data2[common_idx])
                        stats_results['correlation_tests'][f'{col1}_vs_{col2}'] = {
                            'correlation': float(pearson_r),
                            'p_value': float(pearson_p),
                            'significant': pearson_p < 0.05
                        }
        
        # Confidence intervals
        for col in numeric_cols:
            data = self.df[col].dropna()
            mean = data.mean()
            sem = stats.sem(data)
            ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=sem)
            stats_results['confidence_intervals'][col] = {
                'mean': float(mean),
                'lower': float(ci[0]),
                'upper': float(ci[1])
            }
        
        return stats_results
    
    def perform_ml_analysis(self):
        """Stage 13: Machine Learning - NEW - COMPREHENSIVE"""
        ml_results = {
            'problem_type': None,
            'supervised_learning': {'classification': [], 'regression': []},
            'unsupervised_learning': {},
            'feature_engineering': {},
            'model_evaluation': {},
            'implementation_code': ''
        }
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_cols) >= 2:
            # Determine problem type
            ml_results['problem_type'] = 'Regression'
            
            # SUPERVISED LEARNING - REGRESSION
            ml_results['supervised_learning']['regression'] = [
                {
                    'name': 'Linear Regression',
                    'use_case': 'Predict continuous values with linear relationships',
                    'when_to_use': 'When relationship between features and target is linear',
                    'complexity': 'Low',
                    'interpretability': 'High',
                    'pros': 'Fast, interpretable, works well with linear data',
                    'cons': 'Assumes linearity, sensitive to outliers'
                },
                {
                    'name': 'Polynomial Regression',
                    'use_case': 'Capture non-linear relationships',
                    'when_to_use': 'When scatter plots show curved patterns',
                    'complexity': 'Medium',
                    'interpretability': 'Medium',
                    'pros': 'Captures non-linear patterns',
                    'cons': 'Risk of overfitting with high degrees'
                },
                {
                    'name': 'Decision Tree Regressor',
                    'use_case': 'Complex non-linear patterns with interactions',
                    'when_to_use': 'When relationships are complex and feature interactions exist',
                    'complexity': 'Medium',
                    'interpretability': 'High',
                    'pros': 'Handles non-linearity, no feature scaling needed',
                    'cons': 'Prone to overfitting'
                }
            ]
            
            # SUPERVISED LEARNING - CLASSIFICATION (if applicable)
            if len(categorical_cols) > 0:
                ml_results['supervised_learning']['classification'] = [
                    {
                        'name': 'Logistic Regression',
                        'use_case': 'Binary classification with probability estimates',
                        'when_to_use': 'Need probability scores and feature importance',
                        'complexity': 'Low',
                        'interpretability': 'High'
                    },
                    {
                        'name': 'Decision Tree Classifier',
                        'use_case': 'Multi-class classification with interpretable rules',
                        'when_to_use': 'Need to explain decisions to stakeholders',
                        'complexity': 'Medium',
                        'interpretability': 'High'
                    },
                    {
                        'name': 'K-Nearest Neighbors (KNN)',
                        'use_case': 'Pattern matching based on similarity',
                        'when_to_use': 'Similar instances should have similar outcomes',
                        'complexity': 'Low',
                        'interpretability': 'Medium'
                    },
                    {
                        'name': 'Naive Bayes',
                        'use_case': 'Text classification, spam detection',
                        'when_to_use': 'Features are independent or nearly independent',
                        'complexity': 'Low',
                        'interpretability': 'Medium'
                    }
                ]
            
            # UNSUPERVISED LEARNING - K-Means Clustering
            X = self.df[numeric_cols].dropna()
            if len(X) > 10:
                # Elbow method for optimal clusters
                inertias = []
                K_range = range(2, min(11, len(X)//10 + 2))
                for k in K_range:
                    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                    kmeans.fit(X)
                    inertias.append(kmeans.inertia_)
                
                # Perform clustering with optimal k
                optimal_k = 3  # Default
                kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
                clusters = kmeans.fit_predict(X)
                
                ml_results['unsupervised_learning'] = {
                    'algorithm': 'K-Means Clustering',
                    'use_case': 'Customer segmentation, pattern grouping',
                    'features_used': numeric_cols,
                    'optimal_clusters': optimal_k,
                    'inertia': float(kmeans.inertia_),
                    'business_applications': [
                        'Customer Segmentation - Group customers by behavior',
                        'Market Segmentation - Identify market niches',
                        'Anomaly Detection - Find unusual patterns',
                        'Product Categorization - Auto-group similar products'
                    ],
                    'elbow_data': {'k_values': list(K_range), 'inertias': inertias}
                }
            
            # FEATURE ENGINEERING
            ml_results['feature_engineering'] = {
                'important_features': numeric_cols[:5],
                'transformations_needed': [],
                'encoding_strategies': {}
            }
            
            # Check for skewed features
            for col in numeric_cols:
                skewness = abs(self.df[col].skew())
                if skewness > 1:
                    ml_results['feature_engineering']['transformations_needed'].append({
                        'column': col,
                        'issue': f'Highly skewed (skewness: {skewness:.2f})',
                        'recommendation': 'Apply log transformation: np.log1p(df[col])',
                        'reason': 'Reduce skewness for better model performance'
                    })
            
            # Categorical encoding strategies
            for col in categorical_cols:
                unique_count = self.df[col].nunique()
                ml_results['feature_engineering']['encoding_strategies'][col] = {
                    'unique_values': unique_count,
                    'recommended_encoding': 'One-Hot Encoding' if unique_count <= 10 else 'Label Encoding',
                    'code': f"pd.get_dummies(df['{col}'])" if unique_count <= 10 else f"LabelEncoder().fit_transform(df['{col}'])"
                }
            
            # MODEL EVALUATION
            ml_results['model_evaluation'] = {
                'train_test_split': '80/20 or 70/30 recommended',
                'cross_validation': '5-fold or 10-fold cross-validation',
                'regression_metrics': ['R² Score', 'RMSE', 'MAE', 'MAPE'],
                'classification_metrics': ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Confusion Matrix']
            }
            
            # COMPLETE IMPLEMENTATION CODE
            ml_results['implementation_code'] = f'''# COMPLETE MACHINE LEARNING PIPELINE
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('your_data.csv')

# ===== REGRESSION EXAMPLE =====
print("=" * 50)
print("REGRESSION ANALYSIS")
print("=" * 50)

# Prepare features and target
X = df[{numeric_cols[1:3]}]  # Features
y = df['{numeric_cols[0]}']  # Target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Linear Regression
model_lr = LinearRegression()
model_lr.fit(X_train_scaled, y_train)
y_pred_lr = model_lr.predict(X_test_scaled)

print(f"Linear Regression R² Score: {{r2_score(y_test, y_pred_lr):.4f}}")
print(f"RMSE: {{np.sqrt(mean_squared_error(y_test, y_pred_lr)):.4f}}")

# Train Decision Tree
model_dt = DecisionTreeRegressor(random_state=42, max_depth=5)
model_dt.fit(X_train, y_train)
y_pred_dt = model_dt.predict(X_test)

print(f"\nDecision Tree R² Score: {{r2_score(y_test, y_pred_dt):.4f}}")
print(f"RMSE: {{np.sqrt(mean_squared_error(y_test, y_pred_dt)):.4f}}")

# ===== CLUSTERING EXAMPLE =====
print("\n" + "=" * 50)
print("CLUSTERING ANALYSIS")
print("=" * 50)

# Prepare data for clustering
X_cluster = df[{numeric_cols[:3]}].dropna()
X_cluster_scaled = StandardScaler().fit_transform(X_cluster)

# Elbow method
inertias = []
K = range(2, 11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_cluster_scaled)
    inertias.append(kmeans.inertia_)

# Plot elbow curve
plt.figure(figsize=(10, 6))
plt.plot(K, inertias, 'bo-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method For Optimal k')
plt.grid(True)
plt.show()

# Perform clustering with optimal k
optimal_k = 3  # Choose based on elbow curve
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_cluster_scaled)

print(f"\nClustering complete with {{optimal_k}} clusters")
print("\nCluster Statistics:")
for i in range(optimal_k):
    print(f"\nCluster {{i}}:")
    print(df[df['Cluster'] == i][{numeric_cols[:3]}].describe())

# ===== FEATURE IMPORTANCE =====
print("\n" + "=" * 50)
print("FEATURE IMPORTANCE")
print("=" * 50)

feature_importance = pd.DataFrame({{
    'feature': X.columns,
    'importance': model_dt.feature_importances_
}}).sort_values('importance', ascending=False)

print(feature_importance)

print("\n" + "=" * 50)
print("ANALYSIS COMPLETE")
print("=" * 50)
'''
        
        return ml_results
    
    def perform_hypothesis_testing(self):
        """Stage 14: Hypothesis Testing - NEW"""
        hypothesis_results = {'suggested_hypotheses': [], 't_tests': {}, 'regression': {}}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        # Suggested hypotheses
        if len(numeric_cols) > 0:
            hypothesis_results['suggested_hypotheses'].append({
                'h0': f'Mean of {numeric_cols[0]} equals {self.df[numeric_cols[0]].mean():.2f}',
                'h1': 'Mean is different',
                'test': 'One-sample t-test'
            })
        
        # T-test
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            unique_cats = self.df[cat_col].unique()
            
            if len(unique_cats) == 2:
                group1 = self.df[self.df[cat_col] == unique_cats[0]][num_col].dropna()
                group2 = self.df[self.df[cat_col] == unique_cats[1]][num_col].dropna()
                
                if len(group1) > 1 and len(group2) > 1:
                    t_stat, p_value = stats.ttest_ind(group1, group2)
                    hypothesis_results['t_tests'][f'{cat_col}_effect'] = {
                        't_statistic': float(t_stat),
                        'p_value': float(p_value),
                        'significant': p_value < 0.05
                    }
        
        # Linear regression
        if len(numeric_cols) >= 2:
            X = self.df[numeric_cols[1]].dropna()
            y = self.df[numeric_cols[0]].dropna()
            common_idx = X.index.intersection(y.index)
            
            if len(common_idx) > 2:
                X = X[common_idx]
                y = y[common_idx]
                X_with_const = sm.add_constant(X)
                model = sm.OLS(y, X_with_const).fit()
                
                hypothesis_results['regression'] = {
                    'r_squared': float(model.rsquared),
                    'coefficients': {'intercept': float(model.params[0]), 'slope': float(model.params[1])},
                    'equation': f'{numeric_cols[0]} = {model.params[0]:.4f} + {model.params[1]:.4f} * {numeric_cols[1]}'
                }
        
        return hypothesis_results
    
    def generate_ai_insights(self):
        """Stage 15: AI Insights with Gemini - NEW - COMPREHENSIVE"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # Prepare comprehensive data summary
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = self.df.select_dtypes(include=['object']).columns.tolist()
            
            # Calculate key metrics
            key_metrics = {}
            for col in numeric_cols[:5]:
                if any(kw in col.lower() for kw in ['sales', 'revenue', 'profit', 'amount', 'price']):
                    key_metrics[col] = {
                        'total': float(self.df[col].sum()),
                        'average': float(self.df[col].mean()),
                        'median': float(self.df[col].median())
                    }
            
            prompt = f"""You are a SENIOR DATA ANALYST expert with 15+ years of experience. Analyze this dataset comprehensively:

═══════════════════════════════════════════════════════════════════
DATASET OVERVIEW
═══════════════════════════════════════════════════════════════════
Rows: {len(self.df):,}
Columns: {len(self.df.columns)}
Column Names: {', '.join(self.df.columns.tolist())}
Numeric Columns: {', '.join(numeric_cols)}
Categorical Columns: {', '.join(categorical_cols)}

═══════════════════════════════════════════════════════════════════
SAMPLE DATA (First 5 rows)
═══════════════════════════════════════════════════════════════════
{self.df.head(5).to_string()}

═══════════════════════════════════════════════════════════════════
STATISTICAL SUMMARY
═══════════════════════════════════════════════════════════════════
{self.df.describe().to_string()}

═══════════════════════════════════════════════════════════════════
KEY METRICS
═══════════════════════════════════════════════════════════════════
{json.dumps(key_metrics, indent=2)}

═══════════════════════════════════════════════════════════════════
YOUR ANALYSIS MUST INCLUDE:
═══════════════════════════════════════════════════════════════════

1. DATA STORY (2-3 paragraphs):
   - What is the business context of this data?
   - What story does the data tell?
   - What is the overall narrative?

2. KEY INSIGHTS (5-7 specific insights):
   - Use actual numbers from the data
   - Identify hidden patterns
   - Highlight surprising findings
   - Point out trends and anomalies
   - Each insight should be actionable

3. BUSINESS RECOMMENDATIONS (5-7 prioritized actions):
   - Specific, actionable recommendations
   - Prioritize by impact (High/Medium/Low)
   - Include quick wins and long-term strategies
   - Quantify expected impact where possible
   - Format: [Priority] Action - Expected Impact

4. PREDICTIVE OPPORTUNITIES:
   - What can be predicted from this data?
   - Which ML models would work best?
   - Expected business value of predictions
   - Implementation complexity (Low/Medium/High)

5. DATA QUALITY CONCERNS:
   - Any red flags in the data?
   - Missing data patterns
   - Outliers or anomalies
   - What additional data would enhance analysis?

6. STRATEGIC QUESTIONS TO EXPLORE:
   - What questions should stakeholders ask?
   - What deeper analysis is needed?
   - What hypotheses should be tested?

7. COMPETITIVE INSIGHTS:
   - How does this data compare to industry benchmarks?
   - What competitive advantages are revealed?
   - What risks or opportunities exist?

═══════════════════════════════════════════════════════════════════
FORMAT YOUR RESPONSE:
═══════════════════════════════════════════════════════════════════
Use clear headers and bullet points.
Be specific with numbers.
Make it business-focused and actionable.
Write for executives and stakeholders.
"""
            
            response = model.generate_content(prompt)
            return {
                'ai_insights': response.text,
                'generated_by': 'Google Gemini Pro',
                'timestamp': datetime.now().isoformat(),
                'data_summary': {
                    'rows': len(self.df),
                    'columns': len(self.df.columns),
                    'numeric_features': len(numeric_cols),
                    'categorical_features': len(categorical_cols)
                }
            }
        except Exception as e:
            return {
                'ai_insights': f'''AI Insights Generation Failed

Error: {str(e)}

Fallback Analysis:
- Dataset has {len(self.df):,} records and {len(self.df.columns)} columns
- Numeric columns: {len(self.df.select_dtypes(include=[np.number]).columns)}
- Categorical columns: {len(self.df.select_dtypes(include=['object']).columns)}

Please check:
1. Internet connection (Gemini API requires internet)
2. API key validity
3. API quota limits

You can still use other analysis stages for insights.''',
                'generated_by': 'Error',
                'error': str(e)
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
    return render_template('index_enhanced.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        df = load_data(file)
        
        analyst = EnhancedDataAnalyst(df)
        
        result = {}
        
        # Run each stage with error handling
        try:
            result["understanding"] = analyst.understand_data()
        except Exception as e:
            result["understanding"] = {"error": str(e)}
        
        try:
            result["cleaning"] = analyst.clean_data()
        except Exception as e:
            result["cleaning"] = {"error": str(e)}
        
        try:
            result["eda"] = analyst.perform_eda()
        except Exception as e:
            result["eda"] = {"error": str(e)}
        
        try:
            result["charts"] = analyst.generate_visualizations()
        except Exception as e:
            result["charts"] = []
        
        try:
            result["insights"] = analyst.generate_insights()
        except Exception as e:
            result["insights"] = []
        
        try:
            result["excel_formulas"] = analyst.generate_excel_formulas()
        except Exception as e:
            result["excel_formulas"] = {"error": str(e)}
        
        try:
            result["advanced_stats"] = analyst.perform_advanced_statistics()
        except Exception as e:
            result["advanced_stats"] = {"error": str(e)}
        
        try:
            result["ml_analysis"] = analyst.perform_ml_analysis()
        except Exception as e:
            result["ml_analysis"] = {"error": str(e)}
        
        try:
            result["hypothesis_testing"] = analyst.perform_hypothesis_testing()
        except Exception as e:
            result["hypothesis_testing"] = {"error": str(e)}
        
        try:
            result["ai_insights"] = analyst.generate_ai_insights()
        except Exception as e:
            result["ai_insights"] = {"ai_insights": f"AI insights unavailable: {str(e)}", "generated_by": "Error"}
        
        result["executive_summary"] = f"Analyzed {len(df):,} records with 15-stage comprehensive pipeline"
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
