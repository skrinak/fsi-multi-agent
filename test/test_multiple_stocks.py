#!/usr/bin/env python3
"""
Test multiple stocks to ensure the FMP integration is robust.
"""

from stock_price_agent import get_stock_prices

def test_multiple_stocks():
    """Test the function with multiple stocks."""
    
    test_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("🧪 Testing multiple stocks with hybrid API integration")
    print("=" * 60)
    
    for ticker in test_stocks:
        print(f"\n📊 Testing {ticker}...")
        
        try:
            result = get_stock_prices(ticker)
            
            if result.get("status") == "success":
                data = result["data"]
                print(f"✅ {ticker}: ${data['current_price']} | 90d Range: ${data['low_90d']}-${data['high_90d']} | Vol: {data['volume']:,}")
            else:
                print(f"❌ {ticker}: {result.get('message', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ {ticker}: Exception - {e}")
    
    print(f"\n🎉 Multi-stock test completed!")

if __name__ == "__main__":
    test_multiple_stocks()