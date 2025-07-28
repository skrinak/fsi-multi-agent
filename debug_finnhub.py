#!/usr/bin/env python3
"""
Debug script to test Finnhub API calls and identify the exact issue.
"""

import os
import time
from dotenv import load_dotenv
import finnhub

# Load environment variables
load_dotenv()

def test_finnhub_api():
    """Test various Finnhub API endpoints to identify the issue."""
    
    api_key = os.getenv('FINNHUB_API_KEY')
    if not api_key:
        print("❌ FINNHUB_API_KEY not found in environment variables")
        return
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    # Initialize client
    finnhub_client = finnhub.Client(api_key=api_key)
    
    # Test 1: Basic quote (should work on free tier)
    print("\n=== TEST 1: Basic Quote ===")
    try:
        quote = finnhub_client.quote('AMZN')
        print(f"✅ Quote successful: {quote}")
    except Exception as e:
        print(f"❌ Quote failed: {e}")
    
    # Test 2: Company profile (should work on free tier)
    print("\n=== TEST 2: Company Profile ===")
    try:
        profile = finnhub_client.company_profile2(symbol='AMZN')
        print(f"✅ Profile successful: {profile.get('name', 'No name')}")
    except Exception as e:
        print(f"❌ Profile failed: {e}")
    
    # Test 3: Historical candles with different time ranges
    print("\n=== TEST 3: Historical Candles (Recent) ===")
    try:
        # Try just 30 days of data first
        end_time = int(time.time())
        start_time = end_time - (30 * 24 * 60 * 60)  # 30 days ago
        
        print(f"Requesting data from {start_time} to {end_time}")
        candles = finnhub_client.stock_candles('AMZN', 'D', start_time, end_time)
        print(f"✅ Candles successful: status={candles.get('s')}, data_points={len(candles.get('c', []))}")
        
        if candles.get('s') != 'ok':
            print(f"❌ API returned error status: {candles}")
            
    except Exception as e:
        print(f"❌ Candles failed: {e}")
        print(f"Exception type: {type(e)}")
    
    # Test 4: Try a different ticker
    print("\n=== TEST 4: Different Ticker (AAPL) ===")
    try:
        end_time = int(time.time())
        start_time = end_time - (30 * 24 * 60 * 60)  # 30 days ago
        
        candles = finnhub_client.stock_candles('AAPL', 'D', start_time, end_time)
        print(f"✅ AAPL Candles successful: status={candles.get('s')}, data_points={len(candles.get('c', []))}")
        
    except Exception as e:
        print(f"❌ AAPL Candles failed: {e}")
    
    # Test 5: Check API key status
    print("\n=== TEST 5: API Key Info ===")
    try:
        # Try to get general market status which should work
        quote = finnhub_client.quote('MSFT')
        if quote and quote.get('c'):
            print("✅ API key appears to be working (got MSFT quote)")
        else:
            print("❌ API key may have issues (no MSFT quote data)")
    except Exception as e:
        print(f"❌ API key test failed: {e}")

if __name__ == "__main__":
    test_finnhub_api()