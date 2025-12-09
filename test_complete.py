import pandas as pd
from app import DataAnalyst
import json

# Load test data
df = pd.read_csv('test_data.csv')
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

# Create analyst
analyst = DataAnalyst(df)

# Run all stages
print("\n1. Understanding data...")
understanding = analyst.understand_data()
print(f"   Shape: {understanding['shape']}")
print(f"   Columns: {len(understanding['columns'])}")

print("\n2. Cleaning data...")
cleaning = analyst.clean_data()
print(f"   Duplicates removed: {cleaning['duplicates_removed']}")
print(f"   Missing values: {len(cleaning['missing_values'])}")

print("\n3. Performing EDA...")
eda = analyst.perform_eda()
print(f"   Numerical columns: {len(eda.get('numerical_summary', {}))}")
print(f"   Categorical columns: {len(eda.get('categorical_summary', {}))}")

print("\n4. Generating insights...")
insights, detailed = analyst.generate_insights()
print(f"   Insights: {len(insights)}")
print(f"   First insight: {insights[0] if insights else 'None'}")

print("\n5. Generating visualizations...")
charts = analyst.generate_visualizations()
print(f"   Charts generated: {len(charts)}")

print("\n6. Generating Python code...")
code = analyst.generate_python_code('test_data.csv')
print(f"   Code length: {len(code)} characters")

print("\n7. Generating SQL queries...")
sql = analyst.generate_sql_queries()
print(f"   SQL queries: {len(sql)}")

print("\n8. Generating DAX measures...")
dax = analyst.generate_dax_measures()
print(f"   DAX measures: {len(dax)}")

print("\n9. Generating JSON output...")
json_output = analyst.generate_json_output(understanding, cleaning, eda, insights, code, sql, dax)
print(f"   JSON keys: {list(json_output.keys())}")

print("\n10. Generating Excel report...")
wb = analyst.generate_excel_report('test_data.csv')
print(f"   Excel sheets: {wb.sheetnames}")
wb.save('test_complete_report.xlsx')

print("\n11. Generating notebook...")
notebook = analyst.generate_notebook('test_data.csv')
print(f"   Notebook cells: {len(notebook['cells'])}")

print("\n✅ ALL STAGES COMPLETED SUCCESSFULLY!")
print("\nFiles generated:")
print("  - test_complete_report.xlsx")
