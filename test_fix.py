import pandas as pd
import numpy as np
from io import StringIO

# Test data with potential issues
test_csv = """show_id,type,title,director,cast,country,date_added,release_year,rating,duration
s1,Movie,Test Movie,Director A,Actor A,USA,March 30 2021,2014,PG,113 min
s2,Movie,Test Movie 2,Director B,Actor B,India,March 30 2021,2018,13+,110 min"""

# Load test data
df = pd.read_csv(StringIO(test_csv))

# Test the analyst
from app import DataAnalyst

analyst = DataAnalyst(df)

print("Testing understand_data...")
understanding = analyst.understand_data()
print(f"OK Understanding: {understanding['shape']}")

print("\nTesting clean_data...")
cleaning = analyst.clean_data()
print(f"OK Cleaning: {cleaning['duplicates_removed']} duplicates")

print("\nTesting perform_eda...")
eda = analyst.perform_eda()
print(f"OK EDA: {len(eda.get('numerical_summary', {}))} numerical columns")

print("\nTesting generate_insights...")
insights, detailed = analyst.generate_insights()
print(f"OK Insights: {len(insights)} insights generated")

print("\nTesting generate_visualizations...")
charts = analyst.generate_visualizations()
print(f"OK Visualizations: {len(charts)} charts generated")

print("\nTesting generate_python_code...")
code = analyst.generate_python_code('test.csv')
print(f"OK Python code: {len(code)} characters")

print("\nTesting generate_sql_queries...")
sql = analyst.generate_sql_queries()
print(f"OK SQL: {len(sql)} queries")

print("\nTesting generate_dax_measures...")
dax = analyst.generate_dax_measures()
print(f"OK DAX: {len(dax)} measures")

print("\nTesting generate_json_output...")
json_out = analyst.generate_json_output(understanding, cleaning, eda, insights, code, sql, dax)
print(f"OK JSON output generated")

print("\nTesting generate_notebook...")
notebook = analyst.generate_notebook('test.csv')
print(f"OK Notebook: {len(notebook['cells'])} cells")

print("\nALL TESTS PASSED!")
