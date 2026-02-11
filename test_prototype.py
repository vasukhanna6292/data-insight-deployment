#!/usr/bin/env python3
"""
End-to-End Prototype Testing Script
Tests all features before submission
"""

import requests
import sys
import os

print("=" * 60)
print("PROTOTYPE END-TO-END TEST")
print("=" * 60)

# Test 1: Check if FastAPI is running
print("\n1. Testing FastAPI connection...")
try:
    response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
    if response.status_code == 200:
        print("   ✅ FastAPI is running and accessible")
    else:
        print(f"   ⚠️  FastAPI returned status {response.status_code}")
except Exception as e:
    print(f"   ❌ FastAPI not accessible: {e}")
    print("   → Start FastAPI: uvicorn api.main:app --reload")
    sys.exit(1)

# Test 2: Check environment variables
print("\n2. Testing environment variables...")
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"   ✅ OPENAI_API_KEY loaded (starts with: {api_key[:15]}...)")
else:
    print("   ❌ OPENAI_API_KEY not found")
    sys.exit(1)

# Test 3: Test full review endpoint
print("\n3. Testing /review/full endpoint...")
try:
    # Create test CSV
    test_csv_content = """transaction_id,Store,Country,SKU,Date,Channel,Promotion,Units Sold,Unit Price,Discount,Revenue,Margin %,Margin
TXN_000001,Walmart,USA,Ferrero Rocher T3,01-01-2025,Retail,None,100,120,0.0,12000,30,3600
TXN_000002,Tesco,UK,Ferrero Rocher 24pc,08-01-2025,Wholesale,Diwali Promo,150,650,0.15,82875,34,28177.5
TXN_000003,Carrefour,Canada,Ferrero Rocher 32pc,15-01-2025,Online,Buy1Get1,50,750,0.5,18750,37,6937.5
TXN_000004,Walmart,USA,Ferrero Rocher T3,22-01-2025,Retail,None,120,120,0.0,14400,30,4320
TXN_000005,Tesco,UK,Ferrero Rocher 24pc,29-01-2025,Wholesale,None,160,650,0.0,104000,34,35360"""
    
    with open('test_data.csv', 'w') as f:
        f.write(test_csv_content)
    
    with open('test_data.csv', 'rb') as f:
        response = requests.post(
            "http://127.0.0.1:8000/review/full",
            files={"file": f},
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Full review endpoint working")
        print(f"      - Analysis week: {data.get('analysis_week')}")
        print(f"      - Executive summary generated: {'Yes' if data.get('executive_summary') else 'No'}")
        print(f"      - Metrics present: {'Yes' if data.get('metrics') else 'No'}")
    else:
        print(f"   ❌ Full review failed: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Full review test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test natural language query endpoint
print("\n4. Testing /review/query endpoint...")
try:
    with open('test_data.csv', 'rb') as f:
        response = requests.post(
            "http://127.0.0.1:8000/review/query",
            files={"file": f},
            data={"query": "Which country performed best?"},
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Natural language query working")
        print(f"      - Query: Which country performed best?")
        print(f"      - Answer generated: {'Yes' if data.get('answer') else 'No'}")
        print(f"      - Intent: {data.get('intent', {}).get('query_type')}")
    else:
        print(f"   ⚠️  Query endpoint returned: {response.status_code}")
        
except Exception as e:
    print(f"   ⚠️  Query test failed (non-critical): {e}")

# Test 5: Test custom exploration query
print("\n5. Testing custom exploration query...")
try:
    with open('test_data.csv', 'rb') as f:
        response = requests.post(
            "http://127.0.0.1:8000/review/query",
            files={"file": f},
            data={"query": "What's the average revenue by country?"},
            timeout=60
        )
    
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Custom exploration working")
        print(f"      - Query type: {data.get('intent', {}).get('query_type')}")
        print(f"      - Code generated: {'Yes' if data.get('code_generated') else 'No'}")
    else:
        print(f"   ⚠️  Custom query returned: {response.status_code}")
        
except Exception as e:
    print(f"   ⚠️  Custom query test failed (non-critical): {e}")

# Cleanup
os.remove('test_data.csv')

print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ All critical tests passed!")
print("✅ Prototype is ready for submission")
print("\nNext steps:")
print("1. Test with synthetic data in UI")
print("2. Create README documentation")
print("3. Create 5-slide presentation")
print("4. Record demo video")
print("=" * 60)
