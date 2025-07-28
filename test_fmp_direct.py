#!/usr/bin/env python3
"""
Direct test of Financial Modeling Prep API to verify it works for historical data.
"""

import os
import requests
import datetime as dt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_fmp_direct():
    """Test FMP API directly without agent framework."""
    
    print("🔍 Testing Financial Modeling Prep API Direct")
    print("=" * 50)
    
    # Get FMP API key
    fmp_api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    
    if not fmp_api_key or fmp_api_key == 'your_fmp_api_key_here':
        print("❌ FINANCIAL_MODELING_PREP_API_KEY not configured")
        print("\n📋 To get FMP API key:")
        print("1. Go to: https://financialmodelingprep.com/")
        print("2. Sign up for free account")
        print("3. Get your API key from dashboard")
        print("4. Add to .env file: FINANCIAL_MODELING_PREP_API_KEY=your_actual_key")
        print("\n✅ Free tier provides: 250 calls/day, 500MB bandwidth")
        return False
    
    print(f"✅ FMP API Key found: {fmp_api_key[:10]}...")
    
    # Test with AAPL for 90 days of data
    ticker = "AAPL"
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=90)
    
    # FMP historical price endpoint
    fmp_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}"
    params = {
        'from': start_date.strftime('%Y-%m-%d'),
        'to': end_date.strftime('%Y-%m-%d'),
        'apikey': fmp_api_key
    }
    
    print(f"📡 Requesting data for {ticker} from {start_date.date()} to {end_date.date()}")
    print(f"🌐 URL: {fmp_url}")
    
    try:
        response = requests.get(fmp_url, params=params, timeout=10)
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
        
        data = response.json()
        print(f"📋 Response keys: {list(data.keys())}")
        
        historical = data.get('historical', [])
        print(f"📈 Historical data points: {len(historical)}")
        
        if not historical:
            print("❌ No historical data returned")
            return False
        
        # Show first few data points
        print("\n🔍 Sample data (most recent 3 days):")
        for i, day in enumerate(historical[:3]):
            print(f"  {day['date']}: O=${day['open']:.2f} H=${day['high']:.2f} L=${day['low']:.2f} C=${day['close']:.2f} V={day['volume']:,}")
        
        # Calculate 90-day high/low like the agent does
        high_prices = [day['high'] for day in historical if day.get('high')]
        low_prices = [day['low'] for day in historical if day.get('low')]
        
        if high_prices and low_prices:
            high_90d = max(high_prices)
            low_90d = min(low_prices)
            print(f"\n📊 90-day Range: Low=${low_90d:.2f} | High=${high_90d:.2f}")
            print("✅ SUCCESS! FMP API is working correctly for historical data")
            return True
        else:
            print("❌ Could not extract high/low prices")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_fmp_rate_limits():
    """Test FMP rate limits and bandwidth usage."""
    
    print("\n🔍 Testing FMP Rate Limits")
    print("-" * 30)
    
    fmp_api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    if not fmp_api_key:
        print("❌ API key required for rate limit test")
        return False
    
    # Test multiple quick requests
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    success_count = 0
    
    for ticker in tickers:
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}"
            params = {'apikey': fmp_api_key}
            
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    print(f"✅ {ticker}: ${data[0].get('price', 'N/A')}")
                    success_count += 1
                else:
                    print(f"❌ {ticker}: No data")
            else:
                print(f"❌ {ticker}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {ticker}: {e}")
    
    print(f"\n📊 Rate limit test: {success_count}/{len(tickers)} successful")
    return success_count == len(tickers)

if __name__ == "__main__":
    historical_works = test_fmp_direct()
    rate_limit_works = test_fmp_rate_limits()
    
    print("\n" + "=" * 50)
    if historical_works and rate_limit_works:
        print("🎉 ALL TESTS PASSED! FMP API is ready for integration.")
        print("\n📋 Next steps:")
        print("1. Install dependencies: cd Finance-assistant-swarm-agent && uv sync")
        print("2. Test the stock_price_agent.py directly")
    else:
        print("❌ Some tests failed. Check API key and network connection.")