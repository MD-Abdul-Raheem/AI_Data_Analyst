import asyncio
from .profiler import DataProfiler
from .analysis import DataAnalyzer
from .llm import LLMService
from .exporter import Exporter
from .utils import read_file, clean_for_json
from .database import async_session_maker, Job
from sqlalchemy import select
from datetime import datetime
import json

class Orchestrator:
    def __init__(self):
        self.llm = LLMService()
    
    async def process_job(self, job_id: str, file_path: str, filename: str):
        """Main orchestration workflow"""
        async with async_session_maker() as session:
            result = await session.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one()
            
            try:
                # Update status
                job.status = "processing"
                await session.commit()
                
                # 1. Load data
                df = await read_file(file_path)
                
                # 2. Profile
                profiler = DataProfiler(df)
                profile = profiler.profile()
                
                job.rows = profile['shape']['rows']
                job.columns = profile['shape']['columns']
                job.quality_score = profile['quality_score']
                await session.commit()
                
                # 3. Analyze & Clean
                analyzer = DataAnalyzer(df, profile)
                cleaning_report = analyzer.clean()
                analysis = analyzer.analyze()
                
                # 4. LLM Generation (parallel)
                insights, sql, python_code, dax = await asyncio.gather(
                    self.llm.generate_insights(profile, analysis),
                    self.llm.generate_sql(profile),
                    self.llm.generate_python(profile, filename),
                    self.llm.generate_dax(profile)
                )
                
                # 5. Export
                notebook = Exporter.create_notebook(profile, python_code, filename)
                json_output = Exporter.create_json_output(profile, analysis, insights, sql, dax)
                
                # 6. Save result
                result_data = {
                    "profile": profile,
                    "cleaning": cleaning_report,
                    "analysis": analysis,
                    "insights": insights,
                    "sql_queries": sql,
                    "python_code": python_code,
                    "dax_measures": dax,
                    "notebook": notebook,
                    "json_output": json_output
                }
                
                job.result_json = json.dumps(clean_for_json(result_data))
                job.status = "completed"
                job.completed_at = datetime.utcnow()
                await session.commit()
                
            except Exception as e:
                job.status = "failed"
                job.error_message = str(e)
                await session.commit()
                raise
