"""
Configuration file for AI Data Analyst application
"""

import os

class Config:
    """Base configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}
    
    # Analysis settings
    MAX_PREVIEW_ROWS = 10
    MAX_CATEGORICAL_UNIQUE = 100
    OUTLIER_METHOD = 'IQR'  # or 'Z-score'
    IQR_MULTIPLIER = 1.5
    Z_SCORE_THRESHOLD = 3
    
    # Visualization settings
    FIGURE_DPI = 100
    FIGURE_SIZE = (10, 6)
    COLOR_PALETTE = 'viridis'
    
    # Code generation settings
    PYTHON_STYLE = 'PEP8'
    SQL_DIALECT = 'standard'  # standard, mysql, postgresql, bigquery
    
    # Performance settings
    CHUNK_SIZE = 10000  # For large file processing
    MAX_CORRELATION_COLUMNS = 20
    MAX_CHART_CATEGORIES = 20

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Add production-specific settings
    # SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB for testing

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
