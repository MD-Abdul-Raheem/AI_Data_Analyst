import pandas as pd
import numpy as np

class DataProfiler:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def profile(self) -> dict:
        """Generate comprehensive data profile"""
        profile = {
            "shape": {"rows": len(self.df), "columns": len(self.df.columns)},
            "columns": self._profile_columns(),
            "quality_score": self._calculate_quality_score(),
            "memory_mb": float(self.df.memory_usage(deep=True).sum() / 1024**2),
            "duplicates": int(self.df.duplicated().sum())
        }
        return profile
    
    def _profile_columns(self) -> dict:
        """Profile each column"""
        columns = {}
        for col in self.df.columns:
            col_data = self.df[col]
            columns[col] = {
                "dtype": str(col_data.dtype),
                "missing": int(col_data.isnull().sum()),
                "missing_pct": float(col_data.isnull().sum() / len(col_data) * 100),
                "unique": int(col_data.nunique()),
                "cardinality": float(col_data.nunique() / len(col_data)),
                "type": self._infer_type(col_data)
            }
            
            if col_data.dtype in ['int64', 'float64']:
                columns[col].update({
                    "min": float(col_data.min()) if not col_data.isnull().all() else None,
                    "max": float(col_data.max()) if not col_data.isnull().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
                    "median": float(col_data.median()) if not col_data.isnull().all() else None
                })
        return columns
    
    def _infer_type(self, col) -> str:
        """Infer semantic type"""
        if col.dtype in ['int64', 'float64']:
            if col.nunique() < 20 and col.nunique() / len(col) < 0.05:
                return 'categorical_numeric'
            return 'numerical'
        elif col.nunique() == len(col):
            return 'id'
        return 'categorical'
    
    def _calculate_quality_score(self) -> float:
        """Calculate data quality score (0-100)"""
        completeness = (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        uniqueness = (1 - self.df.duplicated().sum() / len(self.df)) * 100
        return float((completeness + uniqueness) / 2)
