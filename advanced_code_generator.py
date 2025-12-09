"""
Advanced Code Generation Module
Professional-grade Python, SQL, and DAX code
"""

import pandas as pd
from typing import Dict, List

class AdvancedCodeGenerator:
    """
    Generates expert-level code for analysis
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    def generate_advanced_python(self, filename: str) -> str:
        """
        Generate professional Python code with advanced analytics
        """
        code = f'''"""
Advanced Data Analysis Script
Generated for: {filename}
Includes: EDA, Statistical Testing, Segmentation, and Predictive Insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. DATA LOADING & INITIAL PROFILING
# ============================================================================

df = pd.read_csv('{filename}')

print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print(f"Shape: {{df.shape}}")
print(f"Memory Usage: {{df.memory_usage(deep=True).sum() / 1024**2:.2f}} MB")
print(f"\\nData Types:\\n{{df.dtypes.value_counts()}}")

# ============================================================================
# 2. DATA QUALITY ASSESSMENT
# ============================================================================

print("\\n" + "="*80)
print("DATA QUALITY REPORT")
print("="*80)

# Missing values
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
print(f"\\nMissing Values:\\n{{missing_pct[missing_pct > 0]}}")

# Duplicates
dup_count = df.duplicated().sum()
print(f"\\nDuplicates: {{dup_count}} ({{dup_count/len(df)*100:.2f}}%)")

# Outliers (IQR method)
numeric_cols = df.select_dtypes(include=[np.number]).columns
outlier_summary = {{}}

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
    if outliers > 0:
        outlier_summary[col] = outliers

print(f"\\nOutliers Detected:\\n{{pd.Series(outlier_summary)}}")

# ============================================================================
# 3. STATISTICAL SUMMARY & DISTRIBUTION ANALYSIS
# ============================================================================

print("\\n" + "="*80)
print("STATISTICAL SUMMARY")
print("="*80)

print(df.describe())

# Skewness and Kurtosis
print("\\nDistribution Characteristics:")
for col in numeric_cols:
    skew = df[col].skew()
    kurt = df[col].kurtosis()
    print(f"{{col}}: Skewness={{skew:.3f}}, Kurtosis={{kurt:.3f}}")

# ============================================================================
# 4. CORRELATION & DRIVER ANALYSIS
# ============================================================================

print("\\n" + "="*80)
print("CORRELATION & DRIVER ANALYSIS")
print("="*80)

if len(numeric_cols) > 1:
    corr_matrix = df[numeric_cols].corr()
    
    # Find strongest correlations
    target_col = numeric_cols[0]
    correlations = corr_matrix[target_col].drop(target_col).abs().sort_values(ascending=False)
    
    print(f"\\nTop Drivers of {{target_col}}:")
    print(correlations.head(5))
    
    # Visualize correlation matrix
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f',
                square=True, linewidths=1, cbar_kws={{"shrink": 0.8}})
    plt.title('Correlation Matrix - Key Drivers', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("\\nCorrelation heatmap saved: correlation_heatmap.png")

# ============================================================================
# 5. SEGMENTATION ANALYSIS
# ============================================================================

print("\\n" + "="*80)
print("SEGMENTATION ANALYSIS")
print("="*80)

categorical_cols = df.select_dtypes(include=['object']).columns

if len(categorical_cols) > 0 and len(numeric_cols) > 0:
    cat_col = categorical_cols[0]
    metric_col = numeric_cols[0]
    
    # Segment performance
    segment_stats = df.groupby(cat_col)[metric_col].agg([
        ('count', 'count'),
        ('mean', 'mean'),
        ('median', 'median'),
        ('std', 'std'),
        ('min', 'min'),
        ('max', 'max')
    ]).round(2)
    
    print(f"\\nPerformance by {{cat_col}}:")
    print(segment_stats)
    
    # ANOVA test
    groups = [group[metric_col].dropna() for name, group in df.groupby(cat_col)]
    if len(groups) > 1:
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"\\nANOVA Test: F-statistic={{f_stat:.4f}}, p-value={{p_value:.4f}}")
        print(f"Interpretation: {{'Significant' if p_value < 0.05 else 'Not significant'}} difference across segments")

# ============================================================================
# 6. ANOMALY DETECTION
# ============================================================================

print("\\n" + "="*80)
print("ANOMALY DETECTION")
print("="*80)

for col in numeric_cols:
    # Z-score method
    z_scores = np.abs(stats.zscore(df[col].dropna()))
    anomalies = np.where(z_scores > 3)[0]
    
    if len(anomalies) > 0:
        print(f"\\n{{col}}: {{len(anomalies)}} anomalies detected (>3 std dev)")
        print(f"Sample values: {{df[col].iloc[anomalies[:5]].tolist()}}")

# ============================================================================
# 7. PREDICTIVE INSIGHTS & RECOMMENDATIONS
# ============================================================================

print("\\n" + "="*80)
print("PREDICTIVE INSIGHTS")
print("="*80)

if len(numeric_cols) >= 2:
    target = numeric_cols[0]
    
    # Simple linear regression for top driver
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import r2_score, mean_absolute_error
    
    driver = correlations.index[0]
    X = df[[driver]].dropna()
    y = df.loc[X.index, target]
    
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    r2 = r2_score(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    
    print(f"\\nPredictive Model: {{target}} ~ {{driver}}")
    print(f"R-squared: {{r2:.3f}}")
    print(f"MAE: {{mae:.2f}}")
    print(f"Coefficient: {{model.coef_[0]:.4f}}")
    print(f"Interpretation: 1 unit increase in {{driver}} → {{model.coef_[0]:.2f}} change in {{target}}")

# ============================================================================
# 8. BUSINESS RECOMMENDATIONS
# ============================================================================

print("\\n" + "="*80)
print("BUSINESS RECOMMENDATIONS")
print("="*80)

recommendations = []

# Recommendation 1: Focus on top drivers
if len(numeric_cols) >= 2:
    top_driver = correlations.index[0]
    recommendations.append(
        f"1. OPTIMIZE {{top_driver}}: Strong correlation ({{correlations.iloc[0]:.3f}}) with {{target}}. "
        f"Prioritize improvements in this area for maximum impact."
    )

# Recommendation 2: Address data quality
if dup_count > len(df) * 0.05:
    recommendations.append(
        f"2. DATA QUALITY: {{dup_count}} duplicates detected. Implement data validation at source."
    )

# Recommendation 3: Segment-specific strategies
if len(categorical_cols) > 0 and len(numeric_cols) > 0:
    top_segment = segment_stats['mean'].idxmax()
    recommendations.append(
        f"3. REPLICATE SUCCESS: {{top_segment}} shows highest performance. "
        f"Analyze and replicate best practices across other segments."
    )

for rec in recommendations:
    print(f"\\n{{rec}}")

print("\\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
'''
        
        return code
    
    def generate_advanced_sql(self) -> List[Dict[str, str]]:
        """
        Generate professional SQL queries
        """
        queries = []
        table_name = "dataset"
        
        # Query 1: KPI Dashboard
        if self.numeric_cols:
            kpi_cols = ', '.join([f"SUM({col}) as total_{col}, AVG({col}) as avg_{col}" 
                                 for col in self.numeric_cols[:3]])
            queries.append({
                "name": "KPI Dashboard - Executive Summary",
                "query": f"""-- Executive KPI Dashboard
SELECT 
    COUNT(*) as total_records,
    COUNT(DISTINCT *) as unique_records,
    {kpi_cols}
FROM {table_name};""",
                "purpose": "High-level KPIs for executive dashboard"
            })
        
        # Query 2: Segmentation Analysis
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            metric_col = self.numeric_cols[0]
            
            queries.append({
                "name": "Segment Performance Analysis",
                "query": f"""-- Segment Performance with Rankings
SELECT 
    {cat_col},
    COUNT(*) as record_count,
    SUM({metric_col}) as total_{metric_col},
    AVG({metric_col}) as avg_{metric_col},
    STDDEV({metric_col}) as std_dev,
    MIN({metric_col}) as min_value,
    MAX({metric_col}) as max_value,
    RANK() OVER (ORDER BY SUM({metric_col}) DESC) as performance_rank
FROM {table_name}
GROUP BY {cat_col}
ORDER BY total_{metric_col} DESC;""",
                "purpose": "Identify top and bottom performing segments"
            })
        
        # Query 3: Anomaly Detection
        if self.numeric_cols:
            metric_col = self.numeric_cols[0]
            
            queries.append({
                "name": "Anomaly Detection - Statistical Outliers",
                "query": f"""-- Detect Statistical Outliers (Z-score > 3)
WITH stats AS (
    SELECT 
        AVG({metric_col}) as mean_val,
        STDDEV({metric_col}) as std_val
    FROM {table_name}
),
z_scores AS (
    SELECT 
        *,
        ABS(({metric_col} - (SELECT mean_val FROM stats)) / 
            (SELECT std_val FROM stats)) as z_score
    FROM {table_name}
)
SELECT *
FROM z_scores
WHERE z_score > 3
ORDER BY z_score DESC;""",
                "purpose": "Identify extreme outliers for investigation"
            })
        
        # Query 4: Cohort Analysis
        if self.datetime_cols and self.numeric_cols:
            date_col = self.datetime_cols[0]
            metric_col = self.numeric_cols[0]
            
            queries.append({
                "name": "Cohort Analysis - Monthly Trends",
                "query": f"""-- Monthly Cohort Performance
SELECT 
    DATE_TRUNC('month', {date_col}) as cohort_month,
    COUNT(*) as cohort_size,
    SUM({metric_col}) as total_{metric_col},
    AVG({metric_col}) as avg_{metric_col},
    LAG(SUM({metric_col})) OVER (ORDER BY DATE_TRUNC('month', {date_col})) as prev_month_total,
    (SUM({metric_col}) - LAG(SUM({metric_col})) OVER (ORDER BY DATE_TRUNC('month', {date_col}))) / 
        LAG(SUM({metric_col})) OVER (ORDER BY DATE_TRUNC('month', {date_col})) * 100 as mom_growth_pct
FROM {table_name}
GROUP BY DATE_TRUNC('month', {date_col})
ORDER BY cohort_month;""",
                "purpose": "Track performance trends and growth rates over time"
            })
        
        # Query 5: Top/Bottom Performers
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            metric_col = self.numeric_cols[0]
            
            queries.append({
                "name": "Top & Bottom Performers Comparison",
                "query": f"""-- Compare Top 10 vs Bottom 10 Performers
WITH ranked AS (
    SELECT 
        {cat_col},
        SUM({metric_col}) as total_{metric_col},
        RANK() OVER (ORDER BY SUM({metric_col}) DESC) as rank_desc,
        RANK() OVER (ORDER BY SUM({metric_col}) ASC) as rank_asc
    FROM {table_name}
    GROUP BY {cat_col}
)
SELECT 
    {cat_col},
    total_{metric_col},
    CASE 
        WHEN rank_desc <= 10 THEN 'Top 10'
        WHEN rank_asc <= 10 THEN 'Bottom 10'
    END as performance_tier
FROM ranked
WHERE rank_desc <= 10 OR rank_asc <= 10
ORDER BY total_{metric_col} DESC;""",
                "purpose": "Identify best and worst performers for targeted strategies"
            })
        
        # Query 6: Data Quality Check
        queries.append({
            "name": "Data Quality Assessment",
            "query": f"""-- Comprehensive Data Quality Report
SELECT 
    'Total Records' as metric,
    COUNT(*) as value
FROM {table_name}
UNION ALL
SELECT 
    'Duplicate Records',
    COUNT(*) - COUNT(DISTINCT *)
FROM {table_name}
UNION ALL
SELECT 
    'Completeness %',
    ROUND((1 - SUM(CASE WHEN * IS NULL THEN 1 ELSE 0 END)::FLOAT / 
           (COUNT(*) * (SELECT COUNT(*) FROM information_schema.columns 
            WHERE table_name = '{table_name}'))) * 100, 2)
FROM {table_name};""",
            "purpose": "Monitor data quality metrics for governance"
        })
        
        return queries
    
    def generate_advanced_dax(self) -> List[Dict[str, str]]:
        """
        Generate professional Power BI DAX measures
        """
        measures = []
        
        # Basic KPIs
        if self.numeric_cols:
            for col in self.numeric_cols[:3]:
                # Total
                measures.append({
                    "name": f"Total {col}",
                    "dax": f"Total {col} = SUM('{col}'[{col}])",
                    "category": "Basic KPI"
                })
                
                # Average
                measures.append({
                    "name": f"Average {col}",
                    "dax": f"Average {col} = AVERAGE('{col}'[{col}])",
                    "category": "Basic KPI"
                })
                
                # YTD
                if self.datetime_cols:
                    measures.append({
                        "name": f"{col} YTD",
                        "dax": f"""{col} YTD = 
CALCULATE(
    SUM('{col}'[{col}]),
    DATESYTD('Date'[Date])
)""",
                        "category": "Time Intelligence"
                    })
                
                # YoY Growth
                if self.datetime_cols:
                    measures.append({
                        "name": f"{col} YoY Growth %",
                        "dax": f"""{col} YoY Growth % = 
VAR CurrentYear = SUM('{col}'[{col}])
VAR PreviousYear = 
    CALCULATE(
        SUM('{col}'[{col}]),
        SAMEPERIODLASTYEAR('Date'[Date])
    )
RETURN
    DIVIDE(CurrentYear - PreviousYear, PreviousYear, 0) * 100""",
                        "category": "Growth Metrics"
                    })
        
        # Segmentation measures
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            metric_col = self.numeric_cols[0]
            
            measures.append({
                "name": f"{metric_col} Market Share %",
                "dax": f"""{metric_col} Market Share % = 
DIVIDE(
    SUM('{metric_col}'[{metric_col}]),
    CALCULATE(
        SUM('{metric_col}'[{metric_col}]),
        ALL('{cat_col}')
    ),
    0
) * 100""",
                "category": "Segmentation"
            })
            
            measures.append({
                "name": f"Rank by {metric_col}",
                "dax": f"""Rank by {metric_col} = 
RANKX(
    ALL('{cat_col}'[{cat_col}]),
    CALCULATE(SUM('{metric_col}'[{metric_col}])),
    ,
    DESC,
    DENSE
)""",
                "category": "Ranking"
            })
        
        # Performance indicators
        if len(self.numeric_cols) >= 2:
            col1, col2 = self.numeric_cols[0], self.numeric_cols[1]
            
            measures.append({
                "name": f"{col1} to {col2} Ratio",
                "dax": f"""{col1} to {col2} Ratio = 
DIVIDE(
    SUM('{col1}'[{col1}]),
    SUM('{col2}'[{col2}]),
    0
)""",
                "category": "Efficiency Metrics"
            })
        
        return measures
