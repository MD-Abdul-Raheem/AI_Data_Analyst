"""
Test script for AI Data Analyst application
Run this to verify the application is working correctly
"""

import requests
import json
import os
import time

BASE_URL = 'http://localhost:5000'
TEST_FILE = 'sample_data.csv'

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_server_running():
    """Test if server is running"""
    print_section("Testing Server Connection")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✓ Server is running")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server: {e}")
        print("\nPlease start the server first:")
        print("  python app.py")
        return False

def test_file_upload():
    """Test file upload analysis"""
    print_section("Testing File Upload Analysis")
    
    if not os.path.exists(TEST_FILE):
        print(f"✗ Test file not found: {TEST_FILE}")
        return None
    
    try:
        with open(TEST_FILE, 'rb') as f:
            print(f"Uploading {TEST_FILE}...")
            start_time = time.time()
            
            response = requests.post(
                f'{BASE_URL}/analyze',
                files={'file': f},
                timeout=60
            )
            
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                print(f"✓ Analysis completed in {elapsed:.2f} seconds")
                return response.json()
            else:
                print(f"✗ Analysis failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
    except Exception as e:
        print(f"✗ Error during file upload: {e}")
        return None

def test_raw_data():
    """Test raw data analysis"""
    print_section("Testing Raw Data Analysis")
    
    raw_data = """Name,Age,City,Salary
John Doe,30,New York,75000
Jane Smith,25,Los Angeles,65000
Bob Johnson,35,Chicago,80000
Alice Williams,28,Houston,70000
Charlie Brown,32,Phoenix,72000"""
    
    try:
        print("Sending raw CSV data...")
        start_time = time.time()
        
        response = requests.post(
            f'{BASE_URL}/analyze',
            data={'raw_data': raw_data},
            timeout=60
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✓ Analysis completed in {elapsed:.2f} seconds")
            return response.json()
        else:
            print(f"✗ Analysis failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"✗ Error during raw data analysis: {e}")
        return None

def validate_response(result):
    """Validate the analysis response"""
    print_section("Validating Response Structure")
    
    required_keys = [
        'understanding', 'cleaning', 'eda', 'insights',
        'python_code', 'sql_queries', 'dax_measures',
        'json_output', 'notebook', 'executive_summary'
    ]
    
    all_valid = True
    for key in required_keys:
        if key in result:
            print(f"✓ {key}: Present")
        else:
            print(f"✗ {key}: Missing")
            all_valid = False
    
    return all_valid

def display_results(result):
    """Display key results from analysis"""
    print_section("Analysis Results Summary")
    
    # Executive Summary
    print("\n📊 Executive Summary:")
    print(f"   {result['executive_summary']}")
    
    # Data Understanding
    if 'understanding' in result:
        shape = result['understanding']['shape']
        print(f"\n📋 Dataset Shape: {shape[0]} rows × {shape[1]} columns")
        print(f"   Memory Usage: {result['understanding']['memory_usage']:.2f} MB")
    
    # Insights
    if 'insights' in result and len(result['insights']) > 0:
        print("\n💡 Key Insights:")
        for i, insight in enumerate(result['insights'][:5], 1):
            print(f"   {i}. {insight}")
    
    # Data Quality
    if 'cleaning' in result:
        print("\n🧹 Data Quality:")
        print(f"   Duplicates Removed: {result['cleaning']['duplicates_removed']}")
        missing = result['cleaning'].get('missing_values', {})
        if missing:
            print(f"   Columns with Missing Values: {len(missing)}")
        outliers = result['cleaning'].get('outliers_detected', {})
        if outliers:
            print(f"   Columns with Outliers: {len(outliers)}")
    
    # Generated Outputs
    print("\n📝 Generated Outputs:")
    if 'python_code' in result:
        lines = result['python_code'].count('\n')
        print(f"   ✓ Python Code: {lines} lines")
    
    if 'sql_queries' in result:
        print(f"   ✓ SQL Queries: {len(result['sql_queries'])} queries")
    
    if 'dax_measures' in result:
        print(f"   ✓ DAX Measures: {len(result['dax_measures'])} measures")
    
    if 'notebook' in result:
        cells = len(result['notebook'].get('cells', []))
        print(f"   ✓ Jupyter Notebook: {cells} cells")

def test_error_handling():
    """Test error handling"""
    print_section("Testing Error Handling")
    
    # Test with no data
    try:
        response = requests.post(f'{BASE_URL}/analyze', timeout=5)
        if response.status_code == 400:
            print("✓ Correctly handles missing data")
        else:
            print(f"✗ Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error during test: {e}")

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  AI DATA ANALYST - TEST SUITE")
    print("="*60)
    print("\nThis script will test the AI Data Analyst application")
    print("Make sure the server is running (python app.py)")
    print("\nStarting tests...\n")
    
    # Test 1: Server connection
    if not test_server_running():
        print("\n❌ Cannot proceed - server is not running")
        return False
    
    # Test 2: File upload
    result1 = test_file_upload()
    if result1:
        validate_response(result1)
        display_results(result1)
    
    # Test 3: Raw data
    result2 = test_raw_data()
    if result2:
        validate_response(result2)
    
    # Test 4: Error handling
    test_error_handling()
    
    # Final summary
    print_section("Test Summary")
    
    tests_passed = 0
    tests_total = 4
    
    if test_server_running():
        tests_passed += 1
    if result1:
        tests_passed += 1
    if result2:
        tests_passed += 1
    
    print(f"\nTests Passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("\n✅ All tests passed! Application is working correctly.")
        print("\nYou can now:")
        print("  1. Open http://localhost:5000 in your browser")
        print("  2. Upload your own datasets")
        print("  3. Explore the analysis results")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "="*60 + "\n")
    
    return tests_passed == tests_total

if __name__ == '__main__':
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        exit(1)
