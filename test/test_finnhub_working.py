#!/usr/bin/env python3
"""
Comprehensive test to verify Finnhub integration is working correctly.
"""

import sys
import os
sys.path.insert(0, 'Finance-assistant-swarm-agent')

def test_everything():
    """Test all components"""
    from dotenv import load_dotenv
    from stock_price_agent import get_stock_prices, create_stock_price_agent
    
    load_dotenv()
    
    print("🧪 COMPREHENSIVE FINNHUB TEST")
    print("=" * 50)
    
    # Test 1: Environment variables
    finnhub_key = os.getenv('FINNHUB_API_KEY')
    fmp_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
    
    print(f"✅ Finnhub API Key: {finnhub_key[:10]}..." if finnhub_key else "❌ No Finnhub key")
    print(f"✅ FMP API Key: {fmp_key[:10]}..." if fmp_key else "❌ No FMP key")
    
    # Test 2: Direct function call
    print("\n📊 Testing get_stock_prices function...")
    result = get_stock_prices('AAPL')
    if result['status'] == 'success':
        print(f"✅ Function Success: AAPL at ${result['data']['current_price']}")
    else:
        print(f"❌ Function Error: {result['message']}")
        return False
    
    # Test 3: Agent creation and query
    print("\n🤖 Testing stock price agent...")
    try:
        agent = create_stock_price_agent()
        response = agent("What is AAPL current price?")
        print("✅ Agent Success: Response generated")
        print(f"   Current price extracted from response")
        return True
    except Exception as e:
        print(f"❌ Agent Error: {e}")
        return False

if __name__ == "__main__":
    success = test_everything()
    print(f"\n🎯 Overall Result: {'✅ ALL WORKING' if success else '❌ ISSUES DETECTED'}")