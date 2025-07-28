#!/usr/bin/env python3
"""
Stock Price Analysis Tool

A command-line tool that uses the Strands Agent SDK and Finnhub API to analyze stock prices.
Provides real-time quotes, historical data, and technical analysis for equity research.
"""

import datetime as dt
import os
import time
from typing import Dict, Union
from dotenv import load_dotenv

# Third-party imports
import finnhub
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import think, http_request

# Load environment variables
load_dotenv()


@tool
def get_stock_prices(ticker: str) -> Union[Dict, str]:
    """
    Fetches current and historical stock price data for a given ticker using Finnhub API.
    
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

        # Get historical data (3 months)
        try:
            # Calculate timestamps for 3 months ago and now
            end_time = int(time.time())
            start_time = end_time - (90 * 24 * 60 * 60)  # 90 days ago
            
            # Get daily candle data
            candles = finnhub_client.stock_candles(ticker, 'D', start_time, end_time)
            
            if not candles or candles.get('s') != 'ok' or not candles.get('c'):
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

        # Extract historical data for 90-day high/low
        high_prices = candles['h']
        low_prices = candles['l']
        volumes = candles['v']
        
        # Calculate 90-day high/low
        high_90d = max(high_prices) if high_prices else daily_high
        low_90d = min(low_prices) if low_prices else daily_low
        
        # Get most recent volume (last trading day)
        latest_volume = int(volumes[-1]) if volumes else 0

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
                "data_source": "Finnhub API",
                "historical_data_points": len(candles.get('c', [])) if candles else 0
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
   - Data Source: Finnhub API
   - Historical Data Points Available
   - Market Session Status
</output_format>

<analysis_guidelines>
- Focus on actionable insights for investment decisions
- Highlight significant price movements or volume spikes
- Provide context for unusual trading patterns
- Note any data limitations or market closure impacts
- Use clear, professional financial terminology
</analysis_guidelines>""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region="us-east-1"),
        tools=[get_stock_prices, http_request, think],
    )


def main():
    """Main function to run the stock price analysis tool with Finnhub integration."""
    # Check for API key before starting
    if not os.getenv('FINNHUB_API_KEY'):
        print("❌ Error: FINNHUB_API_KEY not found in environment variables")
        print("Please add your Finnhub API key to a .env file:")
        print("FINNHUB_API_KEY=your_api_key_here")
        return

    # Create and initialize the agent
    stock_price_agent = create_stock_price_agent()
    stock_price_agent.messages = create_initial_messages()

    print("\n📈 Stock Price Analysis Tool (Finnhub API) 📊")
    print("=" * 50)
    print("Enter stock ticker symbols or company names for analysis")
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
        finally:
            # Reset conversation after each query
            stock_price_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
