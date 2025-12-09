import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame, profile: dict):
        self.df = df
        self.profile = profile
        self.charts = []
    
    def clean(self) -> dict:
        """Clean data and return report"""
        report = {"actions": [], "before": len(self.df), "after": 0}
        
        # Fill missing values
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                col_type = self.profile['columns'][col]['type']
                if col_type == 'numerical':
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                    report['actions'].append(f"{col}: filled with median")
                else:
                    self.df[col].fillna('unknown', inplace=True)
                    report['actions'].append(f"{col}: filled with 'unknown'")
        
        # Remove duplicates
        self.df.drop_duplicates(inplace=True)
        report['after'] = len(self.df)
        report['duplicates_removed'] = report['before'] - report['after']
        
        return report
    
    def analyze(self) -> dict:
        """Perform EDA and generate charts"""
        results = {
            "summary": self.df.describe().to_dict(),
            "correlations": {},
            "charts": []
        }
        
        # Correlation matrix
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr = self.df[numeric_cols].corr()
            results['correlations'] = corr.to_dict()
            results['charts'].append(self._create_heatmap(corr))
        
        # Distribution charts for top 3 numerical columns
        for col in list(numeric_cols)[:3]:
            results['charts'].append(self._create_distribution(col))
        
        # Count plots for top 2 categorical columns
        cat_cols = [c for c, info in self.profile['columns'].items() if info['type'] == 'categorical']
        for col in cat_cols[:2]:
            if self.df[col].nunique() < 20:
                results['charts'].append(self._create_countplot(col))
        
        return results
    
    def _create_heatmap(self, corr) -> dict:
        """Generate correlation heatmap as base64"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Correlation Matrix')
        plt.tight_layout()
        return {"type": "heatmap", "title": "Correlation Matrix", "image": self._fig_to_base64()}
    
    def _create_distribution(self, col) -> dict:
        """Generate distribution plot as base64"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        self.df[col].hist(bins=30, ax=axes[0], edgecolor='black')
        axes[0].set_title(f'{col} Distribution')
        self.df[col].plot.box(ax=axes[1])
        axes[1].set_title(f'{col} Boxplot')
        plt.tight_layout()
        return {"type": "distribution", "title": f"{col} Analysis", "image": self._fig_to_base64()}
    
    def _create_countplot(self, col) -> dict:
        """Generate count plot as base64"""
        plt.figure(figsize=(10, 6))
        top_values = self.df[col].value_counts().head(10)
        sns.barplot(x=top_values.values, y=top_values.index, palette='viridis')
        plt.title(f'Top 10 {col}')
        plt.tight_layout()
        return {"type": "countplot", "title": f"{col} Distribution", "image": self._fig_to_base64()}
    
    def _fig_to_base64(self) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return f"data:image/png;base64,{img_base64}"
