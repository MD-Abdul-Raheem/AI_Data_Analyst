import google.generativeai as genai
import json
import os
from .prompts import INSIGHTS_PROMPT, SQL_PROMPT, PYTHON_PROMPT, DAX_PROMPT

class LLMService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_insights(self, profile: dict, analysis: dict) -> list:
        """Generate business insights"""
        column_details = "\n".join([f"- {col}: {info['type']}, {info['unique']} unique, {info['missing_pct']:.1f}% missing" 
                                     for col, info in profile['columns'].items()])
        
        correlations = "None"
        if analysis.get('correlations'):
            corr_list = []
            for col1, vals in list(analysis['correlations'].items())[:3]:
                for col2, val in list(vals.items())[:3]:
                    if col1 != col2 and abs(val) > 0.5:
                        corr_list.append(f"{col1} <-> {col2}: {val:.2f}")
            correlations = "\n".join(corr_list) if corr_list else "None"
        
        prompt = INSIGHTS_PROMPT.format(
            rows=profile['shape']['rows'],
            columns=profile['shape']['columns'],
            quality_score=profile['quality_score'],
            column_details=column_details,
            correlations=correlations
        )
        
        response = self.model.generate_content(prompt)
        try:
            result = json.loads(response.text)
            return result.get('insights', [])
        except:
            return [response.text]
    
    async def generate_sql(self, profile: dict) -> list:
        """Generate SQL queries"""
        columns = ", ".join(profile['columns'].keys())
        prompt = SQL_PROMPT.format(columns=columns)
        
        response = self.model.generate_content(prompt)
        try:
            result = json.loads(response.text)
            return result.get('queries', [])
        except:
            return [{"name": "Sample Query", "sql": f"SELECT * FROM dataset LIMIT 10;"}]
    
    async def generate_python(self, profile: dict, filename: str) -> str:
        """Generate Python code"""
        columns = ", ".join(profile['columns'].keys())
        prompt = PYTHON_PROMPT.format(filename=filename, columns=columns)
        
        response = self.model.generate_content(prompt)
        try:
            result = json.loads(response.text)
            return result.get('code', response.text)
        except:
            return response.text
    
    async def generate_dax(self, profile: dict) -> list:
        """Generate DAX measures"""
        columns = ", ".join(profile['columns'].keys())
        prompt = DAX_PROMPT.format(columns=columns)
        
        response = self.model.generate_content(prompt)
        try:
            result = json.loads(response.text)
            return result.get('measures', [])
        except:
            return [{"name": "Total Count", "dax": "Total Count = COUNTROWS('Table')"}]
