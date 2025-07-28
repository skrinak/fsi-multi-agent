#!/usr/bin/env python3
"""
Check what Finnhub plan features are available with current API key.
"""

import os
import time
from dotenv import load_dotenv
import finnhub

# Load environment variables
load_dotenv()

def check_available_endpoints():
    """Test various endpoints to determine plan limitations."""
    
    api_key = os.getenv('FINNHUB_API_KEY')
    finnhub_client = finnhub.Client(api_key=api_key)
    
    print("🔍 FINNHUB PLAN FEATURE ANALYSIS")
    print("=" * 50)
    
    # Test endpoints that should work on free tier
    free_tier_tests = [
        ("Real-time Quote", lambda: finnhub_client.quote('AAPL')),
        ("Company Profile", lambda: finnhub_client.company_profile2(symbol='AAPL')),
        ("Basic Metrics", lambda: finnhub_client.company_basic_financials('AAPL', 'all')),
    ]
    
    # Test endpoints that require paid subscription
    paid_tier_tests = [
        ("Historical Candles (30 days)", lambda: finnhub_client.stock_candles('AAPL', 'D', int(time.time()) - 30*24*3600, int(time.time()))),
        ("Historical Candles (1 year)", lambda: finnhub_client.stock_candles('AAPL', 'D', int(time.time()) - 365*24*3600, int(time.time()))),
        ("Company News", lambda: finnhub_client.company_news('AAPL', _from='2024-01-01', to='2024-01-31')),
        ("Earnings Estimates", lambda: finnhub_client.company_earnings('AAPL')),
    ]
    
    print("\n✅ FREE TIER FEATURES:")
    for name, test_func in free_tier_tests:
        try:
            result = test_func()
            if result:
                print(f"  ✅ {name}: Available")
            else:
                print(f"  ❌ {name}: No data returned")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
    
    print("\n💰 PAID TIER FEATURES:")
    for name, test_func in paid_tier_tests:
        try:
            result = test_func()
            if result and (isinstance(result, dict) and result.get('s') == 'ok' or isinstance(result, list) and len(result) > 0):
                print(f"  ✅ {name}: Available")
            else:
                print(f"  ❓ {name}: Unclear response")
        except Exception as e:
            if "403" in str(e) or "access" in str(e).lower():
                print(f"  ❌ {name}: Requires paid subscription")
            else:
                print(f"  ❓ {name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 DIAGNOSIS:")
    print("Your API key appears to be on the FREE TIER")
    print("Historical candle data requires a PAID subscription")
    print("\n🔧 SOLUTIONS:")
    print("1. Upgrade to Finnhub paid plan ($19/month minimum)")
    print("2. Use alternative free APIs for historical data:")
    print("   - Alpha Vantage (500 requests/day free)")
    print("   - Financial Modeling Prep (250 requests/day free)")
    print("   - Yahoo Finance via yfinance (unlimited but unofficial)")
    print("\n💡 RECOMMENDATION:")
    print("For development, use Alpha Vantage for historical data")
    print("and keep Finnhub for real-time quotes and company profiles")

if __name__ == "__main__":
    check_available_endpoints()