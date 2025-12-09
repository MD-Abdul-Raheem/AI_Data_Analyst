import json
from datetime import datetime

class Exporter:
    @staticmethod
    def create_notebook(profile: dict, python_code: str, filename: str) -> dict:
        """Generate Jupyter notebook"""
        cells = [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# AI Data Analyst\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]},
            {"cell_type": "markdown", "metadata": {}, "source": ["## Import Libraries"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "source": ["import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns"]},
            {"cell_type": "markdown", "metadata": {}, "source": ["## Load Data"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "source": [f"df = pd.read_csv('{filename}')\ndf.head()"]},
            {"cell_type": "markdown", "metadata": {}, "source": ["## Analysis Code"]},
            {"cell_type": "code", "execution_count": None, "metadata": {}, "source": [python_code.split('\n')]}
        ]
        
        return {
            "cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
            "nbformat": 4,
            "nbformat_minor": 4
        }
    
    @staticmethod
    def create_json_output(profile: dict, analysis: dict, insights: list, sql: list, dax: list) -> dict:
        """Create unified JSON output"""
        return {
            "summary": {
                "rows": profile['shape']['rows'],
                "columns": profile['shape']['columns'],
                "quality_score": profile['quality_score']
            },
            "insights": insights,
            "sql_queries": sql,
            "dax_measures": dax,
            "profile": profile,
            "analysis": analysis
        }
