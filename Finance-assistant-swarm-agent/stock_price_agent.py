#!/usr/bin/env python3
"""
Stock Price Analysis Tool

A command-line tool that uses hybrid APIs for comprehensive stock analysis:
- Finnhub API: Real-time quotes, company profiles, current market data
- Financial Modeling Prep API: Historical OHLC data and 90-day price ranges
Provides complete technical analysis for equity research with reliable data sources.
"""

import datetime as dt
import os
import time
from typing import Dict, Union
from dotenv import load_dotenv

# STRANDS AGENTS SDK (TOP PRIORITY)
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import think, http_request

# Third-party imports
import finnhub
import requests

# Load environment variables
load_dotenv()


@tool
def get_stock_prices(ticker: str) -> Union[Dict, str]:
    """
    Fetches current and historical stock price data for a given ticker using hybrid API approach.
    Uses Finnhub API for real-time quotes and Financial Modeling Prep for historical data.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with stock price data and analysis or error message
    """
    try:
        # Verify ticker is not empty
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        # Initialize Finnhub client
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"status": "error", "message": "FINNHUB_API_KEY not found in environment variables"}
        

        finnhub_client = finnhub.Client(api_key=api_key)
        ticker = ticker.upper().strip()

        # Get current quote data
        try:
            quote = finnhub_client.quote(ticker)
            if not quote or quote.get('c') is None:
                return {"status": "error", "message": f"No current quote data found for ticker {ticker}"}
        except Exception as e:
            return {"status": "error", "message": f"Error fetching quote data: {str(e)}"}

        # Get historical data (90 days) using Financial Modeling Prep
        try:
            # Get FMP API key
            fmp_api_key = os.getenv('FINANCIAL_MODELING_PREP_API_KEY')
            if not fmp_api_key or fmp_api_key == 'your_fmp_api_key_here':
                return {"status": "error", "message": "FINANCIAL_MODELING_PREP_API_KEY not configured. Sign up at financialmodelingprep.com and add your API key to .env file"}
            
            # Calculate date range for 90 days
            end_date = dt.datetime.now()
            start_date = end_date - dt.timedelta(days=90)
            
            # FMP historical price endpoint
            fmp_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}"
            params = {
                'from': start_date.strftime('%Y-%m-%d'),
                'to': end_date.strftime('%Y-%m-%d'),
                'apikey': fmp_api_key
            }
            
            response = requests.get(fmp_url, params=params, timeout=10)
            if response.status_code != 200:
                return {"status": "error", "message": f"FMP API error: {response.status_code}"}
            
            fmp_data = response.json()
            historical = fmp_data.get('historical', [])
            
            if not historical:
                return {"status": "error", "message": f"No historical data found for ticker {ticker}"}
                
        except Exception as e:
            return {"status": "error", "message": f"Error fetching historical data: {str(e)}"}

        # Extract current data from quote
        current_price = float(quote['c'])  # Current price
        previous_close = float(quote['pc'])  # Previous close
        price_change = float(quote['d'])  # Change
        price_change_percent = float(quote['dp'])  # Percent change
        daily_high = float(quote['h'])  # High price of the day
        daily_low = float(quote['l'])  # Low price of the day
        daily_open = float(quote['o'])  # Open price of the day

        # Extract historical data for 90-day high/low from FMP data
        high_prices = [day['high'] for day in historical if day.get('high')]
        low_prices = [day['low'] for day in historical if day.get('low')]
        volumes = [day['volume'] for day in historical if day.get('volume')]
        
        # Calculate 90-day high/low
        high_90d = max(high_prices) if high_prices else daily_high
        low_90d = min(low_prices) if low_prices else daily_low
        
        # Get most recent volume (most recent day in historical data)
        latest_volume = int(volumes[0]) if volumes else 0  # FMP returns newest first

        return {
            "status": "success",
            "data": {
                "symbol": ticker,
                "current_price": round(current_price, 2),
                "previous_close": round(previous_close, 2),
                "price_change": round(price_change, 2),
                "price_change_percent": round(price_change_percent, 2),
                "daily_high": round(daily_high, 2),
                "daily_low": round(daily_low, 2),
                "daily_open": round(daily_open, 2),
                "volume": latest_volume,
                "high_90d": round(high_90d, 2),
                "low_90d": round(low_90d, 2),
                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                "data_source": "Finnhub + FMP APIs",
                "historical_data_points": len(historical) if historical else 0
            },
        }

    except Exception as e:
        return {"status": "error", "message": f"Error fetching price data: {str(e)}"}


def create_initial_messages():
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "Hello, I need help analyzing stock prices."}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "I'm ready to help you analyze stock prices. Please provide a company name or ticker symbol."
                }
            ],
        },
    ]


def create_stock_price_agent():
    """Create and configure the stock price analysis agent with Finnhub integration."""
    return Agent(
        system_prompt="""You are a stock price analysis specialist using Finnhub API for real-time financial data. Follow these steps:

<input>
When user provides a company name or ticker:
1. Use get_stock_prices to fetch current quote and historical data from Finnhub
2. Analyze price movements, trends, and trading patterns
3. Provide comprehensive analysis in the format below
</input>

<output_format>
1. Current Price Information:
   - Current Price & Previous Close
   - Price Change ($ and %)
   - Daily Range (Open, High, Low)
   - Trading Volume

2. Historical Performance:
   - 90-day High/Low Range
   - Price Trend Analysis
   - Volume Pattern Assessment

3. Technical Analysis Summary:
   - Key Price Levels
   - Momentum Indicators
   - Risk Assessment

4. Data Quality Notes:
   - Real-time Data: Finnhub API
   - Historical Data: Financial Modeling Prep API
   - Market Session Status
</output_format>

<analysis_guidelines>
- Focus on actionable insights for investment decisions
- Highlight significant price movements or volume spikes
- Provide context for unusual trading patterns
- Note any data limitations or market closure impacts
- Use clear, professional financial terminology
</analysis_guidelines>""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
        tools=[get_stock_prices, http_request, think],
    )


def main():
    """Main function to run the stock price analysis tool with hybrid API integration."""
    # Check for required API keys before starting
    missing_keys = []
    if not os.getenv('FINNHUB_API_KEY'):
        missing_keys.append('FINNHUB_API_KEY')
    if not os.getenv('FINANCIAL_MODELING_PREP_API_KEY'):
        missing_keys.append('FINANCIAL_MODELING_PREP_API_KEY')
    
    if missing_keys:
        print(f"❌ Error: Missing API keys: {', '.join(missing_keys)}")
        print("Please add your API keys to a .env file:")
        if 'FINNHUB_API_KEY' in missing_keys:
            print("FINNHUB_API_KEY=your_finnhub_key_here  # Sign up at finnhub.io")
        if 'FINANCIAL_MODELING_PREP_API_KEY' in missing_keys:
            print("FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here  # Sign up at financialmodelingprep.com")
        return

    # Create and initialize the agent
    stock_price_agent = create_stock_price_agent()
    stock_price_agent.messages = create_initial_messages()

    print("\n📈 Stock Price Analysis Tool (Hybrid API) 📊")
    print("=" * 50)
    print("Real-time quotes: Finnhub | Historical data: Financial Modeling Prep")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Stock Symbol/Company> ")

        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy investing!")
            break

        if not query.strip():
            print("Please enter a stock symbol or company name.")
            continue

        print(f"\n🔍 Analyzing {query.upper()}...")
        print("-" * 30)

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [{"text": f"Please analyze the stock price for: {query}"}],
            }

            # Add message to conversation
            stock_price_agent.messages.append(user_message)

            # Get response
            response = stock_price_agent(user_message["content"][0]["text"])
            print(f"{response}\n")

        except Exception as e:
            print(f"❌ Error analyzing {query}: {str(e)}\n")
            
            # Check if it's an API key issue
            if "FINNHUB_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid Finnhub API key")
                break
            elif "FINANCIAL_MODELING_PREP_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid Financial Modeling Prep API key")
                break
        finally:
            # Reset conversation after each query
            stock_price_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
