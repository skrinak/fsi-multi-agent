#!/usr/bin/env python3
"""
Financial Metrics Analysis Tool

A command-line tool that uses the Strands Agent SDK and Finnhub API to analyze financial metrics of stocks.
Provides comprehensive fundamental analysis including ratios, growth metrics, and profitability indicators.
"""

import datetime as dt
import os
from typing import Dict, Union
from dotenv import load_dotenv

# Third-party imports
import finnhub
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from strands_tools import think, http_request

# Load environment variables - check multiple locations
load_dotenv()  # Current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Parent directory


@tool
def get_financial_metrics(ticker: str) -> Union[Dict, str]:
    """
    Fetches comprehensive financial metrics for a given stock ticker using Finnhub API.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with financial metrics and ratios or error message
    """
    try:
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        # Initialize Finnhub client
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"status": "error", "message": "FINNHUB_API_KEY not found in environment variables"}
        
        finnhub_client = finnhub.Client(api_key=api_key)
        ticker = ticker.upper().strip()

        # Get company basic financials
        try:
            basic_financials = finnhub_client.company_basic_financials(ticker, 'all')
            if not basic_financials or not basic_financials.get('metric'):
                return {"status": "error", "message": f"No financial data found for ticker {ticker}"}
        except Exception as e:
            return {"status": "error", "message": f"Error fetching basic financials: {str(e)}"}

        # Get company profile for additional information
        try:
            profile = finnhub_client.company_profile2(symbol=ticker)
            if not profile:
                profile = {}
        except Exception as e:
            profile = {}
            print(f"Warning: Could not fetch company profile: {str(e)}")

        # Extract metrics from Finnhub response
        metric_data = basic_financials.get('metric', {})
        
        # Helper function to safely get and round numeric values
        def safe_get_numeric(data, key, multiplier=1, decimal_places=2):
            value = data.get(key)
            if value is not None and isinstance(value, (int, float)):
                return round(value * multiplier, decimal_places)
            return "N/A"
        
        # Helper function to safely get values without modification
        def safe_get(data, key, default="N/A"):
            value = data.get(key)
            return value if value is not None else default

        # Compile comprehensive financial metrics
        metrics = {
            "status": "success",
            "data": {
                "symbol": ticker,
                "company_name": safe_get(profile, 'name', ticker),
                "market_cap": safe_get_numeric(profile, 'marketCapitalization', 1000000),  # Convert to actual value
                
                # Valuation Ratios
                "pe_ratio": safe_get_numeric(metric_data, 'peBasicExclExtraTTM'),
                "forward_pe": safe_get_numeric(metric_data, 'peNormalizedAnnual'),
                "peg_ratio": safe_get_numeric(metric_data, 'pegRatio'),
                "price_to_book": safe_get_numeric(metric_data, 'pbAnnual'),
                "price_to_sales": safe_get_numeric(metric_data, 'psAnnual'),
                "ev_to_ebitda": safe_get_numeric(metric_data, 'evToEbitdaTTM'),
                
                # Profitability Metrics
                "profit_margins": safe_get_numeric(metric_data, 'netProfitMarginTTM', 100),  # Convert to percentage
                "operating_margin": safe_get_numeric(metric_data, 'operatingMarginTTM', 100),
                "gross_margin": safe_get_numeric(metric_data, 'grossMarginTTM', 100),
                "return_on_equity": safe_get_numeric(metric_data, 'roeTTM', 100),
                "return_on_assets": safe_get_numeric(metric_data, 'roaTTM', 100),
                "return_on_invested_capital": safe_get_numeric(metric_data, 'roicTTM', 100),
                
                # Growth Metrics
                "revenue_growth": safe_get_numeric(metric_data, 'revenueGrowthTTMYoy', 100),
                "earnings_growth": safe_get_numeric(metric_data, 'epsGrowthTTMYoy', 100),
                "revenue_growth_3y": safe_get_numeric(metric_data, 'revenueGrowth3Y', 100),
                "revenue_growth_5y": safe_get_numeric(metric_data, 'revenueGrowth5Y', 100),
                
                # Financial Health
                "current_ratio": safe_get_numeric(metric_data, 'currentRatioAnnual'),
                "quick_ratio": safe_get_numeric(metric_data, 'quickRatioAnnual'),
                "debt_to_equity": safe_get_numeric(metric_data, 'totalDebtToEquityAnnual'),
                "debt_to_assets": safe_get_numeric(metric_data, 'totalDebtToTotalCapitalAnnual'),
                "interest_coverage": safe_get_numeric(metric_data, 'interestCoverageAnnual'),
                
                # Dividend Information
                "dividend_yield": safe_get_numeric(metric_data, 'dividendYieldIndicatedAnnual', 100),
                "dividend_per_share": safe_get_numeric(metric_data, 'dividendPerShareAnnual'),
                "payout_ratio": safe_get_numeric(metric_data, 'payoutRatioAnnual', 100),
                
                # Market Risk
                "beta": safe_get_numeric(metric_data, 'beta'),
                
                # Additional Company Info
                "shares_outstanding": safe_get_numeric(profile, 'shareOutstanding', 1000000),  # Convert to actual shares
                "float_shares": safe_get_numeric(profile, 'shareOutstanding', 1000000),  # Approximation
                
                # Metadata
                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                "data_source": "Finnhub API",
                "currency": safe_get(profile, 'currency', 'USD'),
                "exchange": safe_get(profile, 'exchange', 'Unknown'),
                "country": safe_get(profile, 'country', 'Unknown'),
                "industry": safe_get(profile, 'finnhubIndustry', 'Unknown'),
            }
        }

        return metrics

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching financial metrics: {str(e)}"
        }


def create_initial_messages():
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [
                {"text": "Hello, I need help analyzing company financial metrics and fundamentals."}
            ],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "I'm ready to help you analyze comprehensive financial metrics using Finnhub API. Please provide a company ticker symbol for detailed fundamental analysis."
                }
            ],
        },
    ]


def create_financial_metrics_agent():
    """Create and configure the financial metrics analysis agent with Finnhub integration."""
    return Agent(
        system_prompt="""You are a comprehensive financial analysis specialist using Finnhub API for institutional-grade financial data. Follow these steps:

<input>
When user provides a company ticker:
1. Use get_financial_metrics to fetch comprehensive fundamental data from Finnhub
2. Analyze all available financial metrics and ratios
3. Provide detailed investment-grade analysis in the format below
</input>

<output_format>
1. Company Overview:
   - Company Name & Exchange
   - Market Capitalization & Shares Outstanding
   - Industry & Geographic Location
   - Currency & Exchange Information

2. Valuation Metrics:
   - P/E Ratio (Current & Forward)
   - PEG Ratio & Price-to-Book
   - Price-to-Sales & EV/EBITDA
   - Valuation Assessment vs Industry

3. Profitability Analysis:
   - Profit Margins (Net, Operating, Gross)
   - Return Metrics (ROE, ROA, ROIC)
   - Profitability Trends & Quality

4. Growth Indicators:
   - Revenue Growth (TTM, 3Y, 5Y)
   - Earnings Growth Trends
   - Growth Sustainability Assessment

5. Financial Health:
   - Liquidity Ratios (Current, Quick)
   - Leverage Metrics (Debt-to-Equity, Interest Coverage)
   - Financial Stability Assessment

6. Dividend & Returns:
   - Dividend Yield & Per Share
   - Payout Ratio & Sustainability
   - Total Return Potential

7. Risk Assessment:
   - Beta & Market Risk
   - Financial Risk Factors
   - Investment Risk Rating

8. Investment Summary:
   - Key Strengths & Weaknesses
   - Fundamental Score
   - Investment Recommendation Considerations
</output_format>

<analysis_guidelines>
- Provide institutional-quality fundamental analysis
- Compare metrics to industry benchmarks where possible
- Highlight any unusual or concerning metrics
- Focus on investment decision-making insights
- Use professional financial terminology
- Note data limitations or market conditions affecting analysis
- Provide context for metric interpretation
</analysis_guidelines>""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region="us-east-1"),
        tools=[get_financial_metrics, http_request, think],
    )


def main():
    """Main function to run the financial metrics analysis tool with Finnhub integration."""
    # Check for API key before starting
    if not os.getenv('FINNHUB_API_KEY'):
        print("❌ Error: FINNHUB_API_KEY not found in environment variables")
        print("Please add your Finnhub API key to a .env file:")
        print("FINNHUB_API_KEY=your_api_key_here")
        return

    # Create and initialize the agent
    financial_metrics_agent = create_financial_metrics_agent()
    financial_metrics_agent.messages = create_initial_messages()

    print("\n📊 Financial Metrics Analyzer (Finnhub API) 🔍")
    print("=" * 55)
    print("Enter stock ticker symbols for comprehensive fundamental analysis")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Stock Symbol> ").strip()

        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy analyzing!")
            break

        if not query.strip():
            print("Please enter a stock symbol.")
            continue

        print(f"\n🔍 Analyzing {query.upper()} fundamentals...")
        print("-" * 40)

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [
                    {"text": f"Please provide comprehensive financial metrics analysis for: {query}"}
                ],
            }

            # Add message to conversation
            financial_metrics_agent.messages.append(user_message)

            # Get response
            response = financial_metrics_agent(user_message["content"][0]["text"])
            print(f"{response}\n")

        except Exception as e:
            print(f"❌ Error analyzing {query}: {str(e)}\n")
            
            # Check if it's an API key issue
            if "FINNHUB_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid Finnhub API key")
                break
        finally:
            # Reset conversation after each query
            financial_metrics_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
