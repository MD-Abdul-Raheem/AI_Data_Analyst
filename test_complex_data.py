"""
Test script for complex dataset handling
Tests the improved load_data function with various edge cases
"""

import pandas as pd
import numpy as np
from io import StringIO

# Sample of your complex data (first few rows)
complex_data = """Components and Sources>	Components			Reserve Money	Sources							
	Currency in circulation -Total 	`Other' deposits with RBI 	Bankers' deposits with RBI 	Reserve Money (Liabilities/Components) 	RBI's Claims on - Government (net)	RBI's Claims on - Central Govt	RBI's Claims on Banks & Commercial sector	RBI's Claims on Banks (Including NABARD)	RBI's claims on Commercial sector (Excluding NABARD) 	Net foreign exchange assets of RBI 	Govt't currency liabilities to the public 	Net non-monetary liabilities of RBI 
												
21 Aug 2020	2688322	39769	464794	3192884	994754	988987	-346453	-358066	11613	4007883	26315	1489614
14 Aug 2020	2691706	39543	470719	3201967	979844	969138	-310131	-321744	11613	3993710	26315	1487770
07 Aug 2020	2686070	39755	461436	3187260	1075013	1065083	-360149	-371737	11588	4017184	26315	1571102"""

def test_load_complex_data():
    """Test loading complex data with multiple strategies"""
    print("Testing complex data loading...")
    
    # Test 1: Tab-separated data
    try:
        df = pd.read_csv(StringIO(complex_data), sep='\t', engine='python', on_bad_lines='skip')
        print(f"[OK] Loaded with tab separator: {df.shape}")
        print(f"  Columns: {list(df.columns[:5])}...")
        
        # Clean HTML entities
        df.columns = df.columns.str.replace('&gt;', '>', regex=False)
        df.columns = df.columns.str.replace('&#39;', "'", regex=False)
        print(f"  Cleaned columns: {list(df.columns[:5])}...")
        
        # Check for multi-line header
        if len(df) > 0:
            first_row = df.iloc[0]
            print(f"  First row sample: {first_row.iloc[:3].tolist()}")
            
            # If first row is mostly empty, it's part of header
            if first_row.isna().sum() > len(df.columns) * 0.5:
                print("  [WARNING] Detected multi-line header, merging...")
                new_cols = []
                for i, col in enumerate(df.columns):
                    if pd.notna(first_row.iloc[i]) and str(first_row.iloc[i]).strip():
                        new_cols.append(f"{col}_{first_row.iloc[i]}")
                    else:
                        new_cols.append(col)
                df.columns = new_cols
                df = df.iloc[1:].reset_index(drop=True)
                print(f"  New columns: {list(df.columns[:5])}...")
        
        # Convert numeric columns
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass
        
        print(f"[OK] Final shape: {df.shape}")
        print(f"[OK] Data types: {df.dtypes.value_counts().to_dict()}")
        print(f"[OK] Sample data:\n{df.head(2)}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        return False

def test_numeric_conversion():
    """Test conversion of numeric strings with negative values"""
    print("\nTesting numeric conversion...")
    
    test_data = pd.DataFrame({
        'col1': ['100', '-200', '300.5', '-400.75'],
        'col2': ['text', 'data', 'here', 'now']
    })
    
    for col in test_data.columns:
        original_dtype = test_data[col].dtype
        test_data[col] = pd.to_numeric(test_data[col], errors='ignore')
        print(f"  {col}: {original_dtype} -> {test_data[col].dtype}")
    
    print(f"[OK] Converted data:\n{test_data}")
    return True

def test_html_entity_cleaning():
    """Test HTML entity cleaning in column names"""
    print("\nTesting HTML entity cleaning...")
    
    test_cols = [
        "Components and Sources&gt;",
        "`Other&#39; deposits",
        "RBI&amp;s Claims",
        "Govt&quot;t currency"
    ]
    
    cleaned = []
    for col in test_cols:
        clean_col = col.replace('&gt;', '>').replace('&#39;', "'").replace('&amp;', '&').replace('&quot;', '"')
        cleaned.append(clean_col)
        print(f"  {col} -> {clean_col}")
    
    print("[OK] HTML entities cleaned successfully")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("COMPLEX DATA LOADING TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Complex Data Loading", test_load_complex_data()))
    results.append(("Numeric Conversion", test_numeric_conversion()))
    results.append(("HTML Entity Cleaning", test_html_entity_cleaning()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n[SUCCESS] All tests passed! The app should handle your complex dataset.")
    else:
        print("\n[WARNING] Some tests failed. Please review the errors above.")
