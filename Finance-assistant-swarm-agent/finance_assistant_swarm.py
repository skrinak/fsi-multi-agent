#!/usr/bin/env python3
"""
Finance Assistant Swarm Agent

A collaborative swarm of specialized agents for comprehensive stock analysis using Finnhub API.
Integrates multiple financial analysis agents to provide comprehensive investment research and recommendations.
"""

# Standard library imports
import time
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Third-party imports
from strands import Agent
from strands.models import BedrockModel
from strands_tools import think, http_request

# Load environment variables - check multiple locations
load_dotenv()  # Current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Parent directory

# Third-party imports for ticker validation
import finnhub

# Try to import swarm tools - graceful fallback if not available
try:
    from strands_tools.swarm import Swarm, SwarmAgent
    SWARM_AVAILABLE = True
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
    """
    Validate ticker symbol using Finnhub API.
    
    Args:
        ticker: Stock ticker symbol to validate
        
    Returns:
        Dict with validation status and ticker info
    """
    try:
        # Clean and format ticker
        ticker = ticker.strip().upper()
        
        if not ticker:
            return {"valid": False, "error": "Empty ticker symbol"}
        
        # Check basic format (1-5 letters)
        import re
        if not re.match(r'^[A-Z]{1,5}$', ticker):
            return {"valid": False, "error": f"Invalid ticker format: {ticker}"}
        
        # Get API key
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"valid": False, "error": "FINNHUB_API_KEY not found in environment"}
        
        # Initialize Finnhub client
        finnhub_client = finnhub.Client(api_key=api_key)
        
        # Test ticker with quote endpoint
        quote = finnhub_client.quote(ticker)
        
        # Check if quote contains valid data
        if not quote or 'c' not in quote:
            return {"valid": False, "error": f"No data found for ticker: {ticker}"}
        
        # Finnhub returns 0 for invalid tickers
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


class StockAnalysisSwarm:
    """A collaborative swarm of specialized agents for comprehensive stock analysis using Finnhub API."""

    def __init__(self):
        """Initialize the swarm with specialized financial analysis agents."""
        # Check for API key
        if not os.getenv('FINNHUB_API_KEY'):
            print("⚠️ Warning: FINNHUB_API_KEY not found in environment variables")
            print("Please add your Finnhub API key to a .env file for full functionality")
        
        if not SWARM_AVAILABLE:
            self._init_simple_agents()
            return
        # Initialize Swarm with Nova Pro model
        self.swarm = Swarm(
            task="Analyze company stock with multiple specialized Finnhub-powered agents",
            coordination_pattern="collaborative",
        )

        # Create SwarmAgent instances with Finnhub integration
        self.search_agent = SwarmAgent(
            agent_id="search_agent",
            system_prompt="""You are a company information specialist using Finnhub API.
            Your role is to:
            1. Use get_company_info to find comprehensive company details from Finnhub
            2. Verify company identity and ticker symbols
            3. Share verified company information with other agents
            4. Ensure accuracy and completeness of Finnhub data
            5. Provide context about company industry, market cap, and basic profile""",
            shared_memory=self.swarm.shared_memory,
        )
        self.search_agent.tools = [get_company_info, think]

        self.price_agent = SwarmAgent(
            agent_id="price_agent",
            system_prompt="""You are a stock price analysis specialist using Finnhub API.
            Your role is to:
            1. Analyze current stock prices and real-time quotes from Finnhub
            2. Examine historical price trends and patterns
            3. Assess trading volume and market activity
            4. Share price analysis insights with other agents
            5. Provide technical analysis and price movement context
            Focus on recent price movements, volatility, and trading patterns.""",
            shared_memory=self.swarm.shared_memory,
        )
        self.price_agent.tools = [get_stock_prices, http_request, think]

        self.metrics_agent = SwarmAgent(
            agent_id="metrics_agent",
            system_prompt="""You are a financial metrics specialist using Finnhub API.
            Your role is to:
            1. Analyze comprehensive financial metrics from Finnhub company fundamentals
            2. Evaluate valuation ratios, profitability, and growth metrics
            3. Assess financial health indicators and performance trends
            4. Share financial insights and investment quality analysis with other agents
            5. Provide context on financial strength and investment attractiveness
            Focus on key performance indicators, ratios, and fundamental analysis.""",
            shared_memory=self.swarm.shared_memory,
        )
        self.metrics_agent.tools = [get_financial_metrics, http_request, think]

        self.news_agent = SwarmAgent(
            agent_id="news_agent",
            system_prompt="""You are a news and market sentiment specialist using Finnhub API and web intelligence.
            Your role is to:
            1. Gather recent company news from Finnhub API and multiple web sources
            2. Analyze market sentiment and investor perception
            3. Identify key developments affecting company outlook
            4. Share news insights and sentiment analysis with other agents
            5. Provide context on how news may impact investment decisions
            Focus on recent developments, market sentiment, and news impact assessment.""",
            shared_memory=self.swarm.shared_memory,
        )
        self.news_agent.tools = [get_company_info, get_stock_news, http_request, think]

        # Add agents to swarm with enhanced Finnhub-focused prompts
        self.swarm.add_agent(
            self.search_agent,
            system_prompt="""You are the company information coordinator in the Finnhub-powered swarm.
            Use get_company_info to find and verify comprehensive company information from Finnhub API.
            Share verified company data including market cap, industry, and profile details with other agents.
            Focus on accuracy and completeness of Finnhub institutional-grade data.""",
        )

        self.swarm.add_agent(
            self.price_agent,
            system_prompt="""You are a price analysis specialist in the Finnhub-powered swarm.
            Analyze real-time stock prices, historical trends, and trading patterns using Finnhub data.
            Share comprehensive price analysis including current quotes and technical insights with other agents.
            Focus on recent price movements, volatility analysis, and market timing considerations.""",
        )

        self.swarm.add_agent(
            self.metrics_agent,
            system_prompt="""You are a financial metrics specialist in the Finnhub-powered swarm.
            Analyze comprehensive financial metrics and company fundamentals using Finnhub API.
            Share detailed financial health analysis including valuation, profitability, and growth metrics with other agents.
            Focus on investment-grade fundamental analysis and financial performance indicators.""",
        )

        self.swarm.add_agent(
            self.news_agent,
            system_prompt="""You are a news analysis specialist in the Finnhub-powered swarm.
            Analyze company news from Finnhub API and comprehensive web sources for market sentiment.
            Share news insights, sentiment analysis, and market intelligence with other agents.
            Focus on recent developments, investor sentiment, and news impact on investment outlook.""",
        )
    
    def _init_simple_agents(self):
        """Initialize simple agents when swarm tools are not available."""
        # Create individual agents for direct coordination
        self.search_agent = create_company_analysis_agent()
        self.price_agent = create_stock_price_agent()
        self.metrics_agent = create_financial_metrics_agent()
        self.news_agent = create_company_analysis_agent()
        
        print("Initialized individual agents (swarm tools not available)")

    def analyze_company(self, query: str) -> Dict[str, Any]:
        """Run the swarm analysis for a company using Finnhub-powered agents."""
        try:
            if not SWARM_AVAILABLE:
                return self._simple_analyze_company(query)
            
            # Initialize shared memory with query
            self.swarm.shared_memory.store("query", query)

            # Phase 1: Search for company information
            print("\n🔍 Phase 1: Gathering company information...")
            search_result = self.swarm.process_phase()

            if search_result:
                # Extract ticker and company info
                company_info = search_result[0].get("result", {}).get("content", [{}])[0].get("text", "")
                
                # Try to extract ticker from company info
                ticker = self._extract_ticker_from_info(company_info, query)
                self.swarm.shared_memory.store("ticker", ticker)
                self.swarm.shared_memory.store("company_info", company_info)
                print(f"✅ Found company: {ticker}")

                # Phase 2: Comprehensive Financial Analysis
                print("\n📊 Phase 2: Conducting comprehensive financial analysis...")
                analysis_results = self.swarm.process_phase()

                return {
                    "status": "success",
                    "ticker": ticker,
                    "company_info": company_info,
                    "search_results": search_result,
                    "analysis_results": analysis_results,
                    "shared_memory": self.swarm.shared_memory.get_all_knowledge() if hasattr(self.swarm.shared_memory, 'get_all_knowledge') else {},
                }
            else:
                return {"status": "error", "message": "Failed to find company information"}

        except Exception as e:
            return {"status": "error", "message": f"Swarm analysis error: {str(e)}"}
    
    def _simple_analyze_company(self, query: str) -> Dict[str, Any]:
        """Simple company analysis when swarm tools are not available."""
        try:
            print("\n🔍 Gathering company information...")
            company_info = str(self.search_agent(f"Please find company information for: {query}"))
            
            # Extract ticker
            ticker = self._extract_ticker_from_info(company_info, query)
            
            print(f"\n📊 Analyzing {ticker} with individual agents...")
            
            # Get analysis from each agent
            price_analysis = str(self.price_agent(f"Analyze stock prices for {ticker}"))
            metrics_analysis = str(self.metrics_agent(f"Analyze financial metrics for {ticker}"))
            news_analysis = str(self.news_agent(f"Analyze recent news and sentiment for {ticker}"))
            
            return {
                "status": "success",
                "ticker": ticker,
                "company_info": company_info,
                "price_analysis": price_analysis,
                "metrics_analysis": metrics_analysis,
                "news_analysis": news_analysis,
                "coordination_method": "individual_agents"
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Individual agent analysis error: {str(e)}"}
    
    def _extract_ticker_from_info(self, company_info: str, query: str) -> str:
        """Extract ticker symbol from company information."""
        # Simple extraction logic - look for ticker patterns
        import re
        
        # Look for ticker patterns in the company info
        ticker_patterns = [
            r'ticker[:\s]+([A-Z]{1,5})',
            r'symbol[:\s]+([A-Z]{1,5})',
            r'\b([A-Z]{1,5})\b',  # Any 1-5 letter uppercase word
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, company_info, re.IGNORECASE)
            if matches:
                return matches[0].upper()
        
        # Fallback: use the query itself if it looks like a ticker
        if re.match(r'^[A-Z]{1,5}$', query.upper()):
            return query.upper()
        
        return query.upper()  # Final fallback


def create_orchestration_agent() -> Agent:
    """Create the main orchestration agent that coordinates the Finnhub-powered swarm."""
    # Check for API key before creating orchestration agent
    if not os.getenv('FINNHUB_API_KEY'):
        print("⚠️ Warning: FINNHUB_API_KEY not found - some features may be limited")
    
    swarm_instance = StockAnalysisSwarm()
    
    # Create a proper tool wrapper for the analyze_company method
    from strands import tool
    
    @tool
    def analyze_company_tool(query: str) -> str:
        """Analyze a company using the Finnhub-powered swarm of financial agents."""
        result = swarm_instance.analyze_company(query)
        return str(result)
    
    return Agent(
        system_prompt="""You are a comprehensive stock analysis orchestrator using Finnhub API-powered agents. Your role is to:
        1. Coordinate a swarm of specialized financial analysis agents
        2. Monitor the Finnhub-powered analysis process
        3. Integrate and synthesize findings from multiple data sources
        4. Present institutional-grade investment analysis
        
        When analyzing results, structure the comprehensive report as follows:
        
        1. Executive Summary
           - Investment recommendation (BUY/HOLD/SELL)
           - Key investment thesis
           - Risk assessment summary
        
        2. Company Overview
           - Company name, ticker, and exchange information
           - Industry sector and market capitalization
           - Business description and competitive position
           - Geographic presence and market focus
        
        3. Financial Analysis (Finnhub Data)
           - Current stock price and recent performance
           - Key financial metrics and ratios
           - Profitability and growth indicators
           - Financial health and stability assessment
        
        4. Technical & Price Analysis
           - Current price trends and patterns
           - Trading volume and market activity
           - Technical indicators and momentum
           - Support and resistance levels
        
        5. Market Intelligence
           - Recent news analysis and sentiment
           - Market perception and analyst coverage
           - Key developments and catalysts
           - Industry trends and competitive dynamics
        
        6. Investment Assessment
           - Valuation analysis and price targets
           - Growth prospects and opportunities
           - Risk factors and potential challenges
           - Investment timeline and holding considerations
        
        7. Final Recommendation
           - Clear investment decision with rationale
           - Target price and expected returns
           - Risk mitigation strategies
           - Portfolio allocation suggestions
        
        Focus on providing actionable, professional-grade investment analysis suitable for informed decision-making.""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
        tools=[analyze_company_tool],
    )


def create_initial_messages() -> List[Dict]:
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "Hello, I need help analyzing company stocks."}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "I'm ready to help you analyze companies. Please provide a company name you'd like to analyze."
                }
            ],
        },
    ]


def main():
    """Main function to run the Finnhub-powered finance assistant swarm."""
    # Check for API key at startup
    if not os.getenv('FINNHUB_API_KEY'):
        print("❌ Error: FINNHUB_API_KEY not found in environment variables")
        print("Please add your Finnhub API key to a .env file:")
        print("FINNHUB_API_KEY=your_api_key_here")
        print("\nRunning in limited mode...\n")
    
    # Create the orchestration agent
    orchestration_agent = create_orchestration_agent()

    # Initialize messages for the orchestration agent
    orchestration_agent.messages = create_initial_messages()

    print("\n🏢 Finnhub-Powered Stock Analysis Swarm 📊")
    print("=" * 55)
    print("Comprehensive investment analysis using specialized financial agents")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Company to analyze> ").strip()

        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy investing!")
            break
            
        if not query.strip():
            print("Please enter a company name or ticker symbol.")
            continue

        # Validate ticker if it looks like one (1-5 uppercase letters)
        import re
        if re.match(r'^[A-Z]{1,5}$', query.upper()):
            print(f"\n🔍 Validating ticker symbol {query.upper()}...")
            validation = validate_ticker(query)
            
            if not validation["valid"]:
                print(f"❌ {validation['error']}")
                print("Please enter a valid ticker symbol or company name.")
                continue
            else:
                print(f"✅ {validation['message']}")

        print(f"\n🔍 Initiating comprehensive analysis for {query.upper()}...")
        print("-" * 50)

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [
                    {
                        "text": f"Please conduct a comprehensive investment analysis of {query} using all available Finnhub data and provide a detailed report with clear investment recommendation."
                    }
                ],
            }

            # Add message to conversation
            orchestration_agent.messages.append(user_message)

            # Get response
            response = orchestration_agent(user_message["content"][0]["text"])

            # Format and print response
            print(f"\n📊 Investment Analysis Results for {query.upper()}:")
            print("=" * 60)
            if isinstance(response, dict) and "content" in response:
                for content in response["content"]:
                    if "text" in content:
                        print(content["text"])
            else:
                print(f"{response}")
            print("\n" + "=" * 60)

        except Exception as e:
            print(f"❌ Error analyzing {query}: {str(e)}\n")
            
            # Check for specific error types
            if "FINNHUB_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid Finnhub API key")
                break
            elif "ThrottlingException" in str(e):
                print("⏱️ Rate limit reached. Waiting 5 seconds before retry...")
                time.sleep(5)
                continue
        finally:
            # Reset conversation after each query to maintain clean context
            orchestration_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
