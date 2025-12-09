"""Basic tests for backend components"""
import pytest
import pandas as pd
import numpy as np
from profiler import DataProfiler
from analysis import DataAnalyzer
from utils import clean_for_json

def test_profiler():
    """Test data profiler"""
    df = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'name': ['A', 'B', 'C', 'D', 'E'],
        'value': [10, 20, np.nan, 40, 50]
    })
    
    profiler = DataProfiler(df)
    profile = profiler.profile()
    
    assert profile['shape']['rows'] == 5
    assert profile['shape']['columns'] == 3
    assert 'quality_score' in profile
    assert profile['columns']['value']['missing'] == 1

def test_clean_for_json():
    """Test NaN cleaning"""
    data = {
        'value': np.nan,
        'inf': np.inf,
        'normal': 42,
        'nested': {'nan': np.nan}
    }
    
    cleaned = clean_for_json(data)
    
    assert cleaned['value'] is None
    assert cleaned['inf'] is None
    assert cleaned['normal'] == 42
    assert cleaned['nested']['nan'] is None

def test_analyzer():
    """Test data analyzer"""
    df = pd.DataFrame({
        'a': [1, 2, 3, 4, 5],
        'b': [10, 20, 30, 40, 50]
    })
    
    profile = {'columns': {'a': {'type': 'numerical'}, 'b': {'type': 'numerical'}}}
    analyzer = DataAnalyzer(df, profile)
    
    report = analyzer.clean()
    assert 'actions' in report
    assert report['after'] == 5

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
