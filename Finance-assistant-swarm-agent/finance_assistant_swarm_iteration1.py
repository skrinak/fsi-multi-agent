#!/usr/bin/env python3
"""
Finance Assistant Swarm Agent - Iteration 1: Fix Strands SDK Import
FIXING: Use proper strands.multiagent.Swarm instead of non-existent strands_tools.swarm
"""

# Standard library imports
import time
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# STRANDS AGENTS SDK (TOP PRIORITY)
from strands import Agent
from strands.models import BedrockModel
from strands_tools import think, http_request

# Load environment variables - check multiple locations
load_dotenv()  # Current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Parent directory

# Third-party imports for ticker validation
import finnhub

# ITERATION 1 FIX: Use proper Strands SDK Swarm import
try:
    from strands.multiagent import Swarm
    SWARM_AVAILABLE = True
    print("✅ Iteration 1: Using proper strands.multiagent.Swarm")
except ImportError:
    print("Warning: Swarm tools not available. Using simplified agent coordination.")
    SWARM_AVAILABLE = False

from stock_price_agent import get_stock_prices, create_stock_price_agent
from financial_metrics_agent import (
    get_financial_metrics,
    create_financial_metrics_agent,
)
from company_analysis_agent import (
    get_company_info,
    get_stock_news,
    create_company_analysis_agent,
)


def validate_ticker(ticker: str) -> Dict[str, Any]:
    """Validate ticker symbol using real-time quote API."""
    try:
        ticker = ticker.strip().upper()
        
        if not ticker:
            return {"valid": False, "error": "Empty ticker symbol"}
        
        import re
        if not re.match(r'^[A-Z]{1,5}$', ticker):
            return {"valid": False, "error": f"Invalid ticker format: {ticker}"}
        
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"valid": False, "error": "FINNHUB_API_KEY not found in environment"}
        
        finnhub_client = finnhub.Client(api_key=api_key)
        quote = finnhub_client.quote(ticker)
        
        if not quote or 'c' not in quote:
            return {"valid": False, "error": f"No data found for ticker: {ticker}"}
        
        current_price = quote.get('c', 0)
        if current_price == 0:
            return {"valid": False, "error": f"Invalid or delisted ticker: {ticker}"}
        
        return {
            "valid": True, 
            "ticker": ticker,
            "current_price": current_price,
            "message": f"Valid ticker: {ticker} (${current_price:.2f})"
        }
        
    except Exception as e:
        return {"valid": False, "error": f"Ticker validation failed: {str(e)}"}


class StockAnalysisSwarmIteration1:
    """Iteration 1: Fix basic Swarm import and initialization."""

    def __init__(self):
        """Initialize with proper Strands SDK Swarm."""
        if not os.getenv('FINNHUB_API_KEY'):
            print("⚠️ Warning: FINNHUB_API_KEY not found in environment variables")
            print("Please add your API key to a .env file for full functionality")
        
        if not SWARM_AVAILABLE:
            self._init_simple_agents()
            return
            
        # ITERATION 1 FIX: Create individual agents first
        self._create_individual_agents()
        
        # ITERATION 1 FIX: Use proper Strands SDK Swarm constructor
        self.swarm = Swarm(
            nodes=[
                self.company_info_agent,
                self.price_analysis_agent,
                self.metrics_analysis_agent,
                self.news_analysis_agent
            ],
            max_handoffs=10,
            max_iterations=15,
            execution_timeout=300.0
        )
        
        print("✅ Iteration 1: Created proper Strands SDK Swarm with individual agents")
    
    def _create_individual_agents(self):
        """Create individual agents for the swarm."""
        
        self.company_info_agent = Agent(
            name="company_info_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a company information specialist. 
            Use get_company_info to find comprehensive company details.
            Provide accurate company information including ticker, market cap, and business description.
            
            Your task: When given a company query, fetch the company information and provide it in a structured format.""",
            tools=[get_company_info],
        )
        
        self.price_analysis_agent = Agent(
            name="price_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a stock price analysis specialist.
            Use get_stock_prices to analyze current prices, historical trends, and trading patterns.
            Focus on price movements, volatility, and technical analysis.
            
            Your task: When given a ticker, analyze the stock price data and provide clear price analysis.""",
            tools=[get_stock_prices],
        )
        
        self.metrics_analysis_agent = Agent(
            name="metrics_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a financial metrics specialist.
            Use get_financial_metrics to analyze financial ratios, profitability, and growth indicators.
            Focus on valuation, financial health, and investment quality analysis.
            
            Your task: When given a ticker, analyze the financial metrics and provide comprehensive fundamental analysis.""",
            tools=[get_financial_metrics],
        )
        
        self.news_analysis_agent = Agent(
            name="news_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a news and sentiment specialist.
            Use get_stock_news to analyze recent company news and market sentiment.
            Focus on recent developments and their impact on investment outlook.
            
            Your task: When given a ticker, analyze recent news and provide sentiment analysis.""",
            tools=[get_stock_news],
        )
    
    def _init_simple_agents(self):
        """Initialize simple agents when swarm tools are not available."""
        self.search_agent = create_company_analysis_agent()
        self.price_agent = create_stock_price_agent()
        self.metrics_agent = create_financial_metrics_agent()
        self.news_agent = create_company_analysis_agent()
        
        print("Initialized individual agents (swarm tools not available)")

    def analyze_company(self, query: str) -> Dict[str, Any]:
        """Run swarm analysis - Iteration 1 version."""
        try:
            if not SWARM_AVAILABLE:
                return self._simple_analyze_company(query)
            
            print(f"\n🔍 Iteration 1: Starting swarm analysis for {query}...")
            
            # ITERATION 1 FIX: Use proper Swarm call syntax
            task_prompt = f"""Conduct comprehensive financial analysis for: {query}

Please work together to provide:
1. Company information and profile
2. Stock price analysis and trends  
3. Financial metrics and ratios
4. Recent news and market sentiment

Company/Ticker: {query}"""
            
            # Execute swarm with proper call
            result = self.swarm(task_prompt)
            
            print("✅ Iteration 1: Swarm analysis completed")
            
            return {
                "status": "success",
                "query": query,
                "swarm_response": str(result),
                "coordination_method": "strands_sdk_swarm_iteration1"
            }
                
        except Exception as e:
            print(f"❌ Iteration 1 error: {e}")
            return {"status": "error", "message": f"Swarm analysis error: {str(e)}"}
    
    def _simple_analyze_company(self, query: str) -> Dict[str, Any]:
        """Simple company analysis when swarm tools are not available."""
        try:
            print("\n🔍 Gathering company information...")
            company_info = str(self.search_agent(f"Please find company information for: {query}"))
            
            # Extract ticker
            ticker = self._extract_ticker_from_info(company_info, query)
            
            print(f"\n📊 Analyzing {ticker} with individual agents...")
            
            # PROBLEMATIC SECTION - this causes the jumbled output!
            # All agents run concurrently without synchronization
            price_analysis = str(self.price_agent(f"Analyze stock prices for {ticker}"))
            metrics_analysis = str(self.metrics_agent(f"Analyze financial metrics for {ticker}"))
            news_analysis = str(self.news_agent(f"Analyze recent news and sentiment for {ticker}"))
            
            result = {
                "status": "success",
                "ticker": ticker,
                "company_info": company_info,
                "price_analysis": price_analysis,
                "metrics_analysis": metrics_analysis,
                "news_analysis": news_analysis,
                "coordination_method": "individual_agents"
            }
            return result
            
        except Exception as e:
            return {"status": "error", "message": f"Individual agent analysis error: {str(e)}"}
    
    def _extract_ticker_from_info(self, company_info: str, query: str) -> str:
        """Extract ticker symbol from company information."""
        import re
        
        if re.match(r'^[A-Z]{1,5}$', query.upper().strip()):
            return query.upper().strip()
        
        # Try to find ticker in company info
        ticker_patterns = [
            r'ticker[:\s]+([A-Z]{1,5})',
            r'symbol[:\s]+([A-Z]{1,5})',
            r'\(([A-Z]{1,5})\)',
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, company_info, re.IGNORECASE)
            if matches:
                ticker = matches[0].upper().strip()
                if re.match(r'^[A-Z]{1,5}$', ticker):
                    return ticker
        
        # Known mappings
        company_mappings = {
            'APPLE': 'AAPL', 'MICROSOFT': 'MSFT', 'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN', 'TESLA': 'TSLA', 'NVIDIA': 'NVDA', 'META': 'META'
        }
        
        query_upper = query.upper()
        for company, ticker in company_mappings.items():
            if company in query_upper:
                return ticker
        
        return query.upper().strip()


def main():
    """Test Iteration 1 fixes."""
    print("\n🔧 ITERATION 1: FIXING STRANDS SDK IMPORT")
    print("=" * 60)
    
    swarm = StockAnalysisSwarmIteration1()
    
    print("\nTesting with AAPL...")
    result = swarm.analyze_company("AAPL")
    
    print(f"\nResult Status: {result.get('status')}")
    print(f"Coordination Method: {result.get('coordination_method')}")
    
    if result.get('status') == 'success':
        print("\n--- SWARM RESPONSE ---")
        response = result.get('swarm_response', 'No response')
        print(response[:1000] + "..." if len(response) > 1000 else response)
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")


if __name__ == "__main__":
    main()