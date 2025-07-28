#!/usr/bin/env python3
"""
Simple test of the get_stock_prices function.
"""

from stock_price_agent import get_stock_prices

print("🧪 Testing get_stock_prices with AAPL...")

try:
    result = get_stock_prices("AAPL")
    print(f"Result: {result}")
    
    if result.get("status") == "success":
        data = result["data"]
        print(f"✅ SUCCESS!")
        print(f"Symbol: {data['symbol']}")
        print(f"Current Price: ${data['current_price']}")
        print(f"90-day High: ${data['high_90d']}")
        print(f"90-day Low: ${data['low_90d']}")
        print(f"Volume: {data['volume']:,}")
        print(f"Price Change: {data['price_change']:+.2f} ({data['price_change_percent']:+.2f}%)")
    else:
        print(f"❌ ERROR: {result.get('message', 'Unknown error')}")

except Exception as e:
    print(f"❌ EXCEPTION: {e}")