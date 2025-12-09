"""
Advanced Analytical Techniques Module
Root-cause analysis, hypothesis testing, and predictive insights
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Any

class AdvancedTechniques:
    """
    Advanced analytical techniques beyond basic EDA
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    def perform_root_cause_analysis(self) -> Dict[str, Any]:
        """
        Root-cause analysis using driver decomposition
        """
        root_causes = {
            'primary_drivers': [],
            'contributing_factors': [],
            'interaction_effects': []
        }
        
        if len(self.numeric_cols) >= 2:
            target = self.numeric_cols[0]
            
            # Calculate contribution of each variable
            for col in self.numeric_cols[1:]:
                correlation = self.df[[target, col]].corr().iloc[0, 1]
                if abs(correlation) > 0.3:
                    # Calculate variance explained
                    variance_explained = correlation ** 2
                    
                    root_causes['primary_drivers'].append({
                        'driver': col,
                        'correlation': round(correlation, 3),
                        'variance_explained': round(variance_explained * 100, 1),
                        'impact': 'HIGH' if abs(correlation) > 0.7 else 'MEDIUM' if abs(correlation) > 0.5 else 'LOW',
                        'interpretation': f"{col} explains {variance_explained*100:.1f}% of variance in {target}. "
                                        f"{'Strong' if abs(correlation) > 0.7 else 'Moderate'} {'positive' if correlation > 0 else 'negative'} driver."
                    })
        
        # Categorical drivers
        if self.categorical_cols and self.numeric_cols:
            target = self.numeric_cols[0]
            
            for cat_col in self.categorical_cols[:3]:
                # ANOVA F-test
                groups = [group[target].dropna() for name, group in self.df.groupby(cat_col)]
                if len(groups) > 1 and all(len(g) > 0 for g in groups):
                    f_stat, p_value = stats.f_oneway(*groups)
                    
                    if p_value < 0.05:
                        root_causes['contributing_factors'].append({
                            'factor': cat_col,
                            'f_statistic': round(f_stat, 2),
                            'p_value': round(p_value, 4),
                            'significance': 'SIGNIFICANT' if p_value < 0.01 else 'MODERATE',
                            'interpretation': f"{cat_col} has statistically significant impact on {target} (p={p_value:.4f}). "
                                            f"Different categories show distinct performance levels."
                        })
        
        return root_causes
    
    def detect_anomalies_advanced(self) -> Dict[str, Any]:
        """
        Advanced anomaly detection using statistical methods
        """
        anomalies = {
            'statistical_outliers': [],
            'temporal_anomalies': [],
            'multivariate_anomalies': []
        }
        
        # Z-score based detection
        for col in self.numeric_cols:
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            outlier_indices = np.where(z_scores > 3)[0]
            
            if len(outlier_indices) > 0:
                anomalies['statistical_outliers'].append({
                    'column': col,
                    'count': len(outlier_indices),
                    'percentage': round((len(outlier_indices) / len(self.df)) * 100, 2),
                    'severity': 'HIGH' if len(outlier_indices) > len(self.df) * 0.05 else 'MEDIUM',
                    'values': self.df[col].iloc[outlier_indices[:5]].tolist(),  # Sample
                    'interpretation': f"Detected {len(outlier_indices)} extreme values (>3 standard deviations from mean). "
                                    f"These may represent data errors, exceptional events, or genuine extreme cases requiring investigation."
                })
        
        # IQR-based detection (more robust)
        for col in self.numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 3 * IQR  # Extreme outliers
            upper_bound = Q3 + 3 * IQR
            
            extreme_outliers = ((self.df[col] < lower_bound) | (self.df[col] > upper_bound)).sum()
            
            if extreme_outliers > 0:
                anomalies['multivariate_anomalies'].append({
                    'column': col,
                    'extreme_outliers': int(extreme_outliers),
                    'lower_bound': round(lower_bound, 2),
                    'upper_bound': round(upper_bound, 2),
                    'interpretation': f"Extreme outliers beyond 3×IQR threshold suggest potential data quality issues or exceptional cases."
                })
        
        return anomalies
    
    def perform_cohort_analysis(self) -> Dict[str, Any]:
        """
        Cohort-based analysis for temporal patterns
        """
        cohorts = {
            'cohort_performance': [],
            'retention_patterns': [],
            'insights': []
        }
        
        # Check if we have datetime column
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if datetime_cols and self.numeric_cols:
            date_col = datetime_cols[0]
            metric_col = self.numeric_cols[0]
            
            # Create cohorts by month
            self.df['cohort_month'] = pd.to_datetime(self.df[date_col]).dt.to_period('M')
            
            cohort_data = self.df.groupby('cohort_month')[metric_col].agg([
                ('count', 'count'),
                ('average', 'mean'),
                ('total', 'sum')
            ]).reset_index()
            
            cohort_data['cohort_month'] = cohort_data['cohort_month'].astype(str)
            
            for _, row in cohort_data.iterrows():
                cohorts['cohort_performance'].append({
                    'cohort': row['cohort_month'],
                    'count': int(row['count']),
                    'average': round(row['average'], 2),
                    'total': round(row['total'], 2)
                })
            
            # Calculate month-over-month growth
            if len(cohort_data) > 1:
                cohort_data['mom_growth'] = cohort_data['total'].pct_change() * 100
                avg_growth = cohort_data['mom_growth'].mean()
                
                cohorts['insights'].append(
                    f"Average month-over-month growth: {avg_growth:.1f}%. "
                    f"{'Positive momentum' if avg_growth > 0 else 'Declining trend'} observed across cohorts."
                )
        
        return cohorts
    
    def calculate_kpi_impact(self) -> Dict[str, Any]:
        """
        KPI impact assessment - what drives the key metrics
        """
        impact_analysis = {
            'kpi_drivers': [],
            'sensitivity_analysis': [],
            'optimization_opportunities': []
        }
        
        if len(self.numeric_cols) >= 2:
            target_kpi = self.numeric_cols[0]
            
            # Calculate elasticity for each driver
            for driver in self.numeric_cols[1:]:
                # Calculate correlation
                corr = self.df[[target_kpi, driver]].corr().iloc[0, 1]
                
                if abs(corr) > 0.3:
                    # Estimate elasticity (% change in KPI per 1% change in driver)
                    elasticity = (self.df[target_kpi].std() / self.df[target_kpi].mean()) / \
                                (self.df[driver].std() / self.df[driver].mean()) * corr
                    
                    impact_analysis['kpi_drivers'].append({
                        'driver': driver,
                        'correlation': round(corr, 3),
                        'elasticity': round(elasticity, 3),
                        'impact_level': 'HIGH' if abs(elasticity) > 1 else 'MEDIUM' if abs(elasticity) > 0.5 else 'LOW',
                        'interpretation': f"1% change in {driver} associated with {abs(elasticity):.2f}% change in {target_kpi}. "
                                        f"{'Elastic' if abs(elasticity) > 1 else 'Inelastic'} relationship."
                    })
            
            # Sensitivity analysis - impact of moving drivers by 10%
            for driver_info in impact_analysis['kpi_drivers'][:3]:
                driver = driver_info['driver']
                current_avg = self.df[driver].mean()
                elasticity = driver_info['elasticity']
                
                # Estimate impact of 10% increase
                estimated_impact = elasticity * 10  # 10% change
                
                impact_analysis['sensitivity_analysis'].append({
                    'driver': driver,
                    'scenario': '10% increase',
                    'estimated_kpi_change': f"{estimated_impact:+.1f}%",
                    'recommendation': f"{'Prioritize' if abs(estimated_impact) > 5 else 'Consider'} optimizing {driver} - "
                                    f"high leverage opportunity with {abs(estimated_impact):.1f}% potential KPI impact."
                })
        
        return impact_analysis
    
    def perform_market_basket_analysis(self) -> Dict[str, Any]:
        """
        Market basket analysis for transactional patterns
        """
        basket_analysis = {
            'frequent_combinations': [],
            'association_rules': [],
            'insights': []
        }
        
        # Check if we have categorical columns that could represent items/products
        if len(self.categorical_cols) >= 2:
            cat1, cat2 = self.categorical_cols[0], self.categorical_cols[1]
            
            # Create co-occurrence matrix
            co_occurrence = pd.crosstab(self.df[cat1], self.df[cat2])
            
            # Find top combinations
            combinations = []
            for idx in co_occurrence.index:
                for col in co_occurrence.columns:
                    count = co_occurrence.loc[idx, col]
                    if count > 0:
                        combinations.append({
                            'item1': str(idx),
                            'item2': str(col),
                            'count': int(count),
                            'support': round(count / len(self.df), 4)
                        })
            
            # Sort by count and take top 10
            combinations = sorted(combinations, key=lambda x: x['count'], reverse=True)[:10]
            basket_analysis['frequent_combinations'] = combinations
            
            if combinations:
                basket_analysis['insights'].append(
                    f"Top combination: {combinations[0]['item1']} + {combinations[0]['item2']} "
                    f"appears in {combinations[0]['support']*100:.1f}% of records. "
                    f"Consider bundling or cross-promotion strategies."
                )
        
        return basket_analysis
    
    def generate_forecast_insights(self) -> Dict[str, Any]:
        """
        Forecast-ready observations and trend analysis
        """
        forecast_insights = {
            'trend_analysis': {},
            'seasonality_indicators': [],
            'forecast_recommendations': []
        }
        
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if datetime_cols and self.numeric_cols:
            date_col = datetime_cols[0]
            metric_col = self.numeric_cols[0]
            
            # Aggregate by month
            monthly_data = self.df.set_index(pd.to_datetime(self.df[date_col])).resample('M')[metric_col].mean()
            
            if len(monthly_data) >= 12:
                # Calculate trend
                x = np.arange(len(monthly_data))
                slope, intercept = np.polyfit(x, monthly_data.values, 1)
                
                # Calculate R-squared
                y_pred = slope * x + intercept
                ss_res = np.sum((monthly_data.values - y_pred) ** 2)
                ss_tot = np.sum((monthly_data.values - np.mean(monthly_data.values)) ** 2)
                r_squared = 1 - (ss_res / ss_tot)
                
                forecast_insights['trend_analysis'] = {
                    'slope': round(slope, 4),
                    'direction': 'UPWARD' if slope > 0 else 'DOWNWARD',
                    'strength': 'STRONG' if r_squared > 0.7 else 'MODERATE' if r_squared > 0.4 else 'WEAK',
                    'r_squared': round(r_squared, 3),
                    'interpretation': f"{'Growing' if slope > 0 else 'Declining'} trend with {r_squared*100:.1f}% of variance explained by time. "
                                    f"Trend is {'strong and predictable' if r_squared > 0.7 else 'moderate with some volatility' if r_squared > 0.4 else 'weak with high volatility'}."
                }
                
                # Check for seasonality
                monthly_data_df = monthly_data.to_frame()
                monthly_data_df['month'] = monthly_data_df.index.month
                monthly_avg = monthly_data_df.groupby('month')[metric_col].mean()
                
                # Calculate coefficient of variation across months
                cv = monthly_avg.std() / monthly_avg.mean()
                
                if cv > 0.2:
                    peak_month = monthly_avg.idxmax()
                    low_month = monthly_avg.idxmin()
                    
                    forecast_insights['seasonality_indicators'].append({
                        'pattern': 'SEASONAL',
                        'peak_month': int(peak_month),
                        'low_month': int(low_month),
                        'variation': round(cv * 100, 1),
                        'interpretation': f"Significant seasonal pattern detected (CV={cv*100:.1f}%). "
                                        f"Peak in month {peak_month}, trough in month {low_month}. "
                                        f"Plan inventory and resources accordingly."
                    })
                
                # Forecast recommendations
                if r_squared > 0.5:
                    forecast_insights['forecast_recommendations'].append(
                        "Strong trend component makes time-series forecasting viable. "
                        "Consider ARIMA, exponential smoothing, or Prophet models."
                    )
                
                if cv > 0.2:
                    forecast_insights['forecast_recommendations'].append(
                        "Seasonal patterns detected. Incorporate seasonal decomposition in forecasting models. "
                        "Use seasonal ARIMA (SARIMA) or seasonal exponential smoothing."
                    )
        
        return forecast_insights
