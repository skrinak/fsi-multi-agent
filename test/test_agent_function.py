#!/usr/bin/env python3
"""
Direct test of the stock_price_agent get_stock_prices function.
"""

import sys
sys.path.append('.')

# Set up the path for uv environment
import subprocess
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_stock_price_function():
    """Test the get_stock_prices function directly."""
    
    print("🧪 Testing get_stock_prices function with AAPL")
    print("=" * 50)
    
    # Use uv to run the test in the correct environment
    test_code = '''
import sys
sys.path.append('.')
from stock_price_agent import get_stock_prices

result = get_stock_prices("AAPL")
print("Result:", result)

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
'''
    
    # Write the test code to a temporary file
    with open('temp_test.py', 'w') as f:
        f.write(test_code)
    
    try:
        # Run the test using uv
        result = subprocess.run(['uv', 'run', 'python', 'temp_test.py'], 
                              capture_output=True, text=True, cwd='.')
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        return result.returncode == 0
        
    finally:
        # Clean up
        if os.path.exists('temp_test.py'):
            os.remove('temp_test.py')

if __name__ == "__main__":
    success = test_stock_price_function()
    
    if success:
        print("\n🎉 Stock price agent function test PASSED!")
    else:
        print("\n❌ Stock price agent function test FAILED!")
        sys.exit(1)