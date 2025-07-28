#!/usr/bin/env python3
"""
Test script to verify Financial Modeling Prep integration works correctly.
"""

import os
import sys
sys.path.append('Finance-assistant-swarm-agent')

from dotenv import load_dotenv

# Import the function directly
try:
    from stock_price_agent import get_stock_prices
except ImportError:
    # If direct import fails, try adding the path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Finance-assistant-swarm-agent'))
    from stock_price_agent import get_stock_prices

# Load environment variables
load_dotenv()

def test_fmp_integration():
    """Test the FMP integration for historical data."""
    
    print("🔍 Testing Financial Modeling Prep Integration")
    print("=" * 50)
    
    # Check API keys
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    fmp_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    
    print(f"✅ Finnhub API Key: {'Found' if finnhub_key else '❌ Missing'}")
    print(f"✅ FMP API Key: {'Found' if fmp_key else '❌ Missing'}")
    
    if not finnhub_key:
        print("\n❌ FINNHUB_API_KEY is required for real-time quotes")
        return False
        
    if not fmp_key:
        print("\n❌ FINANCIAL_MODELING_PREP_API_KEY is required for historical data")
        print("Sign up at: https://financialmodelingprep.com/")
        return False
    
    # Test with AAPL
    print(f"\n🧪 Testing with AAPL...")
    try:
        result = get_stock_prices("AAPL")
        
        if result.get('status') == 'success':
            data = result['data']
            print("✅ SUCCESS! Retrieved data:")
            print(f"   Symbol: {data['symbol']}")
            print(f"   Current Price: ${data['current_price']}")
            print(f"   90-day High: ${data['high_90d']}")
            print(f"   90-day Low: ${data['low_90d']}")
            print(f"   Volume: {data['volume']:,}")
            return True
        else:
            print(f"❌ FAILED: {result.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        return False

def test_error_handling():
    """Test error handling for missing API keys."""
    
    print("\n🧪 Testing Error Handling...")
    
    # Temporarily remove FMP key
    original_fmp_key = os.environ.pop('FINANCIAL_MODELING_PREP_API_KEY', None)
    
    try:
        result = get_stock_prices("MSFT")
        if result.get('status') == 'error' and 'FINANCIAL_MODELING_PREP_API_KEY' in result.get('message', ''):
            print("✅ Error handling works correctly")
            return True
        else:
            print("❌ Error handling not working as expected")
            return False
    finally:
        # Restore the key
        if original_fmp_key:
            os.environ['FINANCIAL_MODELING_PREP_API_KEY'] = original_fmp_key

if __name__ == "__main__":
    success = test_fmp_integration()
    error_handling_works = test_error_handling()
    
    print("\n" + "=" * 50)
    if success and error_handling_works:
        print("🎉 ALL TESTS PASSED! FMP integration is working correctly.")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        sys.exit(1)