"""
Advanced Professional Data Analyst Module
Provides deep analytical capabilities beyond basic EDA
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Any

class AdvancedAnalyst:
    """
    Advanced Professional Data Analyst
    Goes beyond EDA with critical thinking, hypothesis testing, and business insights
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        self.datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
    def generate_executive_summary(self) -> Dict[str, Any]:
        """
        1. EXECUTIVE SUMMARY
        Clear, concise, business-focused summary
        """
        summary = {
            'overview': '',
            'key_findings': [],
            'business_impact': '',
            'data_reliability_score': 0
        }
        
        # Calculate data reliability score (1-10)
        completeness = 1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))
        duplicates_pct = self.df.duplicated().sum() / len(self.df)
        reliability_score = round((completeness * 0.6 + (1 - duplicates_pct) * 0.4) * 10, 1)
        
        summary['data_reliability_score'] = reliability_score
        
        # Generate overview
        summary['overview'] = f"""
This dataset contains {len(self.df):,} records across {len(self.df.columns)} dimensions, 
spanning {len(self.numeric_cols)} numerical metrics and {len(self.categorical_cols)} categorical attributes.
Data reliability score: {reliability_score}/10 - {'Excellent' if reliability_score >= 8 else 'Good' if reliability_score >= 6 else 'Fair'}.
        """.strip()
        
        # Identify key findings
        if self.numeric_cols:
            # Find highest variance metric
            variances = self.df[self.numeric_cols].var()
            high_var_col = variances.idxmax()
            summary['key_findings'].append(
                f"High variability detected in {high_var_col} (CV: {(self.df[high_var_col].std() / self.df[high_var_col].mean()):.2%}), "
                f"indicating significant performance dispersion requiring segmentation analysis."
            )
        
        if self.categorical_cols:
            # Find concentration in categorical variables
            for col in self.categorical_cols[:2]:
                top_pct = (self.df[col].value_counts().iloc[0] / len(self.df)) * 100
                if top_pct > 50:
                    summary['key_findings'].append(
                        f"Market concentration: {top_pct:.1f}% of records belong to single {col} category, "
                        f"suggesting potential monopolistic patterns or data collection bias."
                    )
        
        summary['business_impact'] = "Analysis reveals actionable opportunities for performance optimization, risk mitigation, and strategic resource allocation."
        
        return summary
    
    def assess_data_quality(self) -> Dict[str, Any]:
        """
        2. DATA QUALITY & PROFILING
        Deep assessment with interpretation
        """
        quality_report = {
            'missing_values': {},
            'duplicates': {},
            'outliers': {},
            'anomalies': [],
            'data_reliability_score': 0,
            'quality_issues': []
        }
        
        # Missing values analysis
        missing = self.df.isnull().sum()
        for col in missing[missing > 0].index:
            missing_pct = (missing[col] / len(self.df)) * 100
            quality_report['missing_values'][col] = {
                'count': int(missing[col]),
                'percentage': round(missing_pct, 2),
                'severity': 'CRITICAL' if missing_pct > 30 else 'HIGH' if missing_pct > 10 else 'MEDIUM' if missing_pct > 5 else 'LOW',
                'interpretation': self._interpret_missing(col, missing_pct)
            }
        
        # Duplicates
        dup_count = self.df.duplicated().sum()
        quality_report['duplicates'] = {
            'count': int(dup_count),
            'percentage': round((dup_count / len(self.df)) * 100, 2),
            'interpretation': f"{'Significant' if dup_count > len(self.df) * 0.05 else 'Minimal'} duplication detected. "
                            f"{'Investigate data collection process.' if dup_count > len(self.df) * 0.05 else 'Within acceptable range.'}"
        }
        
        # Outliers with interpretation
        for col in self.numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((self.df[col] < (Q1 - 1.5 * IQR)) | (self.df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > 0:
                outlier_pct = (outliers / len(self.df)) * 100
                quality_report['outliers'][col] = {
                    'count': int(outliers),
                    'percentage': round(outlier_pct, 2),
                    'lower_bound': round(Q1 - 1.5 * IQR, 2),
                    'upper_bound': round(Q3 + 1.5 * IQR, 2),
                    'interpretation': self._interpret_outliers(col, outlier_pct)
                }
        
        # Detect anomalies
        quality_report['anomalies'] = self._detect_anomalies()
        
        # Calculate overall reliability score
        completeness = 1 - (self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns)))
        duplicates_score = 1 - (dup_count / len(self.df))
        outlier_score = 1 - (sum([v['count'] for v in quality_report['outliers'].values()]) / (len(self.df) * len(self.numeric_cols))) if self.numeric_cols else 1
        
        quality_report['data_reliability_score'] = round((completeness * 0.4 + duplicates_score * 0.3 + outlier_score * 0.3) * 10, 1)
        
        return quality_report
    
    def calculate_key_metrics(self) -> Dict[str, Any]:
        """
        3. KEY METRICS & KPIs
        Computed and explained
        """
        metrics = {
            'primary_kpis': [],
            'derived_metrics': [],
            'performance_indicators': []
        }
        
        # Identify KPI columns
        kpi_keywords = ['sales', 'revenue', 'profit', 'amount', 'price', 'cost', 'margin', 'value']
        
        for col in self.numeric_cols:
            if any(kw in col.lower() for kw in kpi_keywords):
                kpi_data = {
                    'name': col,
                    'total': float(self.df[col].sum()),
                    'average': float(self.df[col].mean()),
                    'median': float(self.df[col].median()),
                    'std_dev': float(self.df[col].std()),
                    'coefficient_of_variation': float(self.df[col].std() / self.df[col].mean()) if self.df[col].mean() != 0 else 0,
                    'interpretation': self._interpret_kpi(col, self.df[col])
                }
                metrics['primary_kpis'].append(kpi_data)
        
        # Calculate derived metrics
        if len(metrics['primary_kpis']) >= 2:
            # Calculate efficiency ratios
            for i, kpi1 in enumerate(metrics['primary_kpis']):
                for kpi2 in metrics['primary_kpis'][i+1:]:
                    if 'cost' in kpi2['name'].lower() and kpi2['total'] != 0:
                        efficiency = kpi1['total'] / kpi2['total']
                        metrics['derived_metrics'].append({
                            'name': f"{kpi1['name']}_per_{kpi2['name']}",
                            'value': round(efficiency, 2),
                            'interpretation': f"Efficiency ratio of {efficiency:.2f} indicates {kpi1['name']} generation per unit of {kpi2['name']}"
                        })
        
        return metrics
    
    def generate_deep_insights(self) -> List[Dict[str, Any]]:
        """
        4. DEEP INSIGHTS & PATTERNS
        Evidence-based insights with explanations and actions
        """
        insights = []
        
        # Insight 1: Performance Distribution
        if self.numeric_cols:
            primary_metric = self.numeric_cols[0]
            skewness = self.df[primary_metric].skew()
            
            insights.append({
                'insight': f"{primary_metric} distribution is {'right-skewed' if skewness > 0.5 else 'left-skewed' if skewness < -0.5 else 'approximately normal'}",
                'evidence': f"Skewness coefficient: {skewness:.3f}. Mean: {self.df[primary_metric].mean():.2f}, Median: {self.df[primary_metric].median():.2f}",
                'explanation': self._explain_skewness(skewness, primary_metric),
                'action': self._recommend_action_for_skewness(skewness, primary_metric)
            })
        
        # Insight 2: Segmentation opportunity
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            num_col = self.numeric_cols[0]
            
            segment_performance = self.df.groupby(cat_col)[num_col].agg(['mean', 'std', 'count'])
            top_segment = segment_performance['mean'].idxmax()
            bottom_segment = segment_performance['mean'].idxmin()
            performance_gap = (segment_performance.loc[top_segment, 'mean'] / segment_performance.loc[bottom_segment, 'mean'] - 1) * 100
            
            insights.append({
                'insight': f"Significant performance disparity across {cat_col} segments",
                'evidence': f"Top segment ({top_segment}) outperforms bottom segment ({bottom_segment}) by {performance_gap:.1f}%",
                'explanation': f"This {performance_gap:.1f}% gap suggests systematic differences in operational efficiency, market conditions, or resource allocation across segments.",
                'action': f"Conduct root-cause analysis on {top_segment} to identify replicable success factors. Implement targeted improvement programs for {bottom_segment}."
            })
        
        # Insight 3: Correlation-based drivers
        if len(self.numeric_cols) >= 2:
            corr_matrix = self.df[self.numeric_cols].corr()
            target_col = self.numeric_cols[0]
            correlations = corr_matrix[target_col].drop(target_col).abs().sort_values(ascending=False)
            
            if len(correlations) > 0 and correlations.iloc[0] > 0.5:
                driver_col = correlations.index[0]
                corr_value = corr_matrix.loc[target_col, driver_col]
                
                insights.append({
                    'insight': f"{driver_col} is a key driver of {target_col}",
                    'evidence': f"Correlation coefficient: {corr_value:.3f} ({'positive' if corr_value > 0 else 'negative'} relationship)",
                    'explanation': f"Strong {'positive' if corr_value > 0 else 'inverse'} correlation suggests that changes in {driver_col} are associated with {'proportional' if corr_value > 0 else 'inverse'} changes in {target_col}. However, correlation does not imply causation - external factors may influence both variables.",
                    'action': f"Prioritize optimization of {driver_col} as a lever for improving {target_col}. Conduct controlled experiments to establish causal relationship."
                })
        
        # Insight 4: Temporal patterns (if datetime exists)
        if self.datetime_cols and self.numeric_cols:
            date_col = self.datetime_cols[0]
            metric_col = self.numeric_cols[0]
            
            self.df[date_col] = pd.to_datetime(self.df[date_col])
            monthly_trend = self.df.set_index(date_col).resample('M')[metric_col].mean()
            
            if len(monthly_trend) > 3:
                trend_slope = np.polyfit(range(len(monthly_trend)), monthly_trend.values, 1)[0]
                trend_direction = 'upward' if trend_slope > 0 else 'downward'
                
                insights.append({
                    'insight': f"{metric_col} shows {trend_direction} trend over time",
                    'evidence': f"Trend slope: {trend_slope:.2f} per month. {'Growth' if trend_slope > 0 else 'Decline'} rate: {abs(trend_slope / monthly_trend.mean()) * 100:.1f}% monthly",
                    'explanation': f"The {trend_direction} trajectory indicates {'improving' if trend_slope > 0 else 'deteriorating'} performance. This could be driven by market dynamics, operational changes, or seasonal factors.",
                    'action': f"{'Sustain momentum through continued investment' if trend_slope > 0 else 'Implement turnaround strategy to reverse decline'}. Decompose trend into seasonal and cyclical components for deeper understanding."
                })
        
        return insights
    
    def perform_segmentation_analysis(self) -> Dict[str, Any]:
        """
        5. SEGMENTATION ANALYSIS
        Multi-dimensional breakdown
        """
        segmentation = {
            'by_category': [],
            'by_time': [],
            'by_performance': [],
            'recommendations': []
        }
        
        if self.categorical_cols and self.numeric_cols:
            cat_col = self.categorical_cols[0]
            metric_col = self.numeric_cols[0]
            
            # Category-based segmentation
            segment_stats = self.df.groupby(cat_col)[metric_col].agg([
                ('count', 'count'),
                ('total', 'sum'),
                ('average', 'mean'),
                ('median', 'median'),
                ('std_dev', 'std')
            ]).round(2)
            
            for segment in segment_stats.index:
                segmentation['by_category'].append({
                    'segment': str(segment),
                    'count': int(segment_stats.loc[segment, 'count']),
                    'total': float(segment_stats.loc[segment, 'total']),
                    'average': float(segment_stats.loc[segment, 'average']),
                    'median': float(segment_stats.loc[segment, 'median']),
                    'std_dev': float(segment_stats.loc[segment, 'std_dev']),
                    'market_share': round((segment_stats.loc[segment, 'total'] / segment_stats['total'].sum()) * 100, 1)
                })
        
        # Performance-based segmentation (quartiles)
        if self.numeric_cols:
            metric_col = self.numeric_cols[0]
            self.df['performance_quartile'] = pd.qcut(self.df[metric_col], q=4, labels=['Bottom 25%', 'Lower-Mid 25%', 'Upper-Mid 25%', 'Top 25%'])
            
            quartile_stats = self.df.groupby('performance_quartile')[metric_col].agg(['count', 'mean', 'min', 'max'])
            
            for quartile in quartile_stats.index:
                segmentation['by_performance'].append({
                    'quartile': str(quartile),
                    'count': int(quartile_stats.loc[quartile, 'count']),
                    'average': round(quartile_stats.loc[quartile, 'mean'], 2),
                    'range': f"{quartile_stats.loc[quartile, 'min']:.2f} - {quartile_stats.loc[quartile, 'max']:.2f}"
                })
        
        return segmentation
    
    # Helper methods
    def _interpret_missing(self, col: str, pct: float) -> str:
        if pct > 30:
            return f"CRITICAL: {pct:.1f}% missing data in {col} severely compromises analysis reliability. Consider excluding this variable or implementing advanced imputation."
        elif pct > 10:
            return f"HIGH: {pct:.1f}% missing data may introduce bias. Investigate missingness pattern (MCAR, MAR, MNAR) before imputation."
        elif pct > 5:
            return f"MEDIUM: {pct:.1f}% missing data is manageable with appropriate imputation strategy."
        else:
            return f"LOW: {pct:.1f}% missing data has minimal impact on analysis."
    
    def _interpret_outliers(self, col: str, pct: float) -> str:
        if pct > 10:
            return f"High outlier concentration ({pct:.1f}%) suggests data quality issues, measurement errors, or genuine extreme events requiring investigation."
        elif pct > 5:
            return f"Moderate outlier presence ({pct:.1f}%) - verify if outliers represent legitimate extreme values or data errors."
        else:
            return f"Normal outlier distribution ({pct:.1f}%) - likely represents natural variation in {col}."
    
    def _detect_anomalies(self) -> List[str]:
        anomalies = []
        
        # Check for constant columns
        for col in self.df.columns:
            if self.df[col].nunique() == 1:
                anomalies.append(f"Column '{col}' has constant value - provides no analytical value")
        
        # Check for suspicious patterns
        for col in self.numeric_cols:
            if (self.df[col] == 0).sum() > len(self.df) * 0.5:
                anomalies.append(f"Column '{col}' has >50% zero values - investigate data collection process")
        
        return anomalies
    
    def _interpret_kpi(self, col: str, series: pd.Series) -> str:
        cv = series.std() / series.mean() if series.mean() != 0 else 0
        if cv > 1:
            return f"High variability (CV={cv:.2f}) indicates inconsistent performance requiring standardization"
        elif cv > 0.5:
            return f"Moderate variability (CV={cv:.2f}) suggests room for performance optimization"
        else:
            return f"Low variability (CV={cv:.2f}) indicates stable, predictable performance"
    
    def _explain_skewness(self, skew: float, col: str) -> str:
        if skew > 0.5:
            return f"Right skew indicates most {col} values cluster below the mean, with few high-value outliers pulling the average up. This suggests a 'long tail' of high performers."
        elif skew < -0.5:
            return f"Left skew indicates most {col} values cluster above the mean, with few low-value outliers pulling the average down. This may indicate a performance floor or minimum threshold."
        else:
            return f"Symmetric distribution suggests balanced performance across the range, with mean and median closely aligned."
    
    def _recommend_action_for_skewness(self, skew: float, col: str) -> str:
        if abs(skew) > 0.5:
            return f"Consider log transformation for modeling. Investigate drivers of extreme values. Implement targeted strategies for tail segments."
        else:
            return f"Distribution suitable for standard statistical methods. Focus on reducing variance to improve consistency."
