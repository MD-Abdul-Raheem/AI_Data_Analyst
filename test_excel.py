import pandas as pd
import numpy as np
from io import StringIO
from app import DataAnalyst

# Test data
test_csv = """show_id,type,title,sales,profit,quantity,rating
s1,Movie,Test Movie,1000,200,10,4.5
s2,Movie,Test Movie 2,1500,300,15,4.8
s3,TV Show,Test Show,800,150,8,4.2"""

df = pd.read_csv(StringIO(test_csv))
analyst = DataAnalyst(df)

# Run analysis
print("Running analysis...")
analyst.understand_data()
analyst.clean_data()
analyst.perform_eda()

# Generate Excel
print("Generating Excel report...")
wb = analyst.generate_excel_report('test.csv')
wb.save('test_professional_report.xlsx')

print("Excel report generated successfully!")
print("Sheets created:")
for sheet in wb.sheetnames:
    print(f"  - {sheet}")
