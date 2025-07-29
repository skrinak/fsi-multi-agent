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
    from strands_tools.swarm import Swarm
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
        # Create individual agents for the swarm  
        from strands import Agent
        from strands.models.bedrock import BedrockModel

        # Create specialized agents as regular Agent instances with unique names
        self.search_agent = Agent(
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a company information specialist using Finnhub API.
            Use get_company_info to find comprehensive company details from Finnhub.
            Provide accurate company information including ticker, market cap, and business description.""",
            tools=[get_company_info]
        )
        self.search_agent.name = "company_info_specialist"

        self.price_agent = Agent(
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a stock price analysis specialist using Finnhub API.
            Use get_stock_prices to analyze current prices, historical trends, and trading patterns.
            Focus on price movements, volatility, and technical analysis.""",
            tools=[get_stock_prices]
        )
        self.price_agent.name = "stock_price_analyst"

        self.metrics_agent = Agent(
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a financial metrics specialist using Finnhub API.
            Use get_financial_metrics to analyze financial ratios, profitability, and growth indicators.
            Focus on valuation, financial health, and investment quality analysis.""",
            tools=[get_financial_metrics]
        )
        self.metrics_agent.name = "financial_metrics_expert"

        self.news_agent = Agent(
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a news and sentiment specialist using Finnhub API.
            Use get_stock_news to analyze recent company news and market sentiment.
            Focus on recent developments and their impact on investment outlook.""",
            tools=[get_stock_news]
        )
        self.news_agent.name = "news_sentiment_analyst"

        # Initialize Swarm with the correct API for the UV environment version
        self.swarm = Swarm(
            task="Analyze company stock with multiple specialized Finnhub-powered agents",
            coordination_pattern="collaborative"
        )
        
        # Add agents to swarm by creating SwarmAgent instances (UV environment API)
        self.search_swarm_agent = self.swarm.add_agent(
            agent_id="company_info_specialist",
            system_prompt="""You are a company information specialist using Finnhub API.
            Use get_company_info to find comprehensive company details from Finnhub.
            Provide accurate company information including ticker, market cap, and business description."""
        )
        
        self.price_swarm_agent = self.swarm.add_agent(
            agent_id="stock_price_analyst", 
            system_prompt="""You are a stock price analysis specialist using Finnhub API.
            Use get_stock_prices to analyze current prices, historical trends, and trading patterns.
            Focus on price movements, volatility, and technical analysis."""
        )
        
        self.metrics_swarm_agent = self.swarm.add_agent(
            agent_id="financial_metrics_expert",
            system_prompt="""You are a financial metrics specialist using Finnhub API.
            Use get_financial_metrics to analyze financial ratios, profitability, and growth indicators.
            Focus on valuation, financial health, and investment quality analysis."""
        )
        
        self.news_swarm_agent = self.swarm.add_agent(
            agent_id="news_sentiment_analyst",
            system_prompt="""You are a news and sentiment specialist using Finnhub API.
            Use get_stock_news to analyze recent company news and market sentiment.
            Focus on recent developments and their impact on investment outlook."""
        )
        
        # Assign tools to the SwarmAgent instances
        self.search_swarm_agent.tools = [get_company_info]
        self.price_swarm_agent.tools = [get_stock_prices]
        self.metrics_swarm_agent.tools = [get_financial_metrics]
        self.news_swarm_agent.tools = [get_stock_news]
    
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
        print(f"🔧 DEBUG: StockAnalysisSwarm.analyze_company called with query='{query}'")
        print(f"🔧 DEBUG: SWARM_AVAILABLE={SWARM_AVAILABLE}")
        try:
            if not SWARM_AVAILABLE:
                print("🔧 DEBUG: Using _simple_analyze_company (swarm not available)")
                return self._simple_analyze_company(query)
            
            # Use the actual Swarm API with process_phase (UV environment version)
            print("\n🔍 Phase 1: Gathering company information...")
            print(f"🔧 DEBUG: Setting up swarm analysis for query: '{query}'")
            
            # Set the company query in shared memory if available
            if hasattr(self.swarm, 'shared_memory'):
                self.swarm.shared_memory.store("query", query)
                print(f"🔧 DEBUG: Stored query in shared memory")
            
            # Process Phase 1: Company information gathering
            tool_context = {"query": query, "task": "company_info_gathering"}
            print(f"🔧 DEBUG: Calling swarm.process_phase() for phase 1 with context: {tool_context}")
            phase1_result = self.swarm.process_phase(tool_context)
            print(f"🔧 DEBUG: Phase 1 result: {type(phase1_result)}")
            
            if phase1_result:
                # Extract ticker from the first result
                ticker = self._extract_ticker_from_info(str(phase1_result), query)
                print(f"🔧 DEBUG: Extracted ticker: '{ticker}'")
                
                # Store ticker for phase 2
                if hasattr(self.swarm, 'shared_memory'):
                    self.swarm.shared_memory.store("ticker", ticker)
                
                # Process Phase 2: Comprehensive analysis
                print("\n📊 Phase 2: Conducting comprehensive financial analysis...")
                tool_context_phase2 = {"query": query, "ticker": ticker, "task": "comprehensive_analysis"}
                print(f"🔧 DEBUG: Calling swarm.process_phase() for phase 2 with context: {tool_context_phase2}")
                phase2_result = self.swarm.process_phase(tool_context_phase2)
                print(f"🔧 DEBUG: Phase 2 result: {type(phase2_result)}")
                
                return {
                    "status": "success",
                    "ticker": ticker,
                    "swarm_response": str(phase2_result),
                    "phase1_result": str(phase1_result),
                    "coordination_method": "swarm_process_phase"
                }
            else:
                print(f"🔧 DEBUG: Phase 1 returned no results")
                return {"status": "error", "message": "Swarm phase 1 analysis returned no response"}

        except Exception as e:
            return {"status": "error", "message": f"Swarm analysis error: {str(e)}"}
    
    def _simple_analyze_company(self, query: str) -> Dict[str, Any]:
        """Simple company analysis when swarm tools are not available."""
        print(f"🔧 DEBUG: _simple_analyze_company called with query='{query}'")
        try:
            print("\n🔍 Gathering company information...")
            print(f"🔧 DEBUG: Calling search_agent with query: 'Please find company information for: {query}'")
            company_info = str(self.search_agent(f"Please find company information for: {query}"))
            print(f"🔧 DEBUG: search_agent returned {len(company_info)} chars")
            
            # Extract ticker
            print(f"🔧 DEBUG: Extracting ticker from company_info and query '{query}'")
            ticker = self._extract_ticker_from_info(company_info, query)
            print(f"🔧 DEBUG: Extracted ticker: '{ticker}'")
            
            print(f"\n📊 Analyzing {ticker} with individual agents...")
            
            # Get analysis from each agent
            print(f"🔧 DEBUG: Calling price_agent for ticker '{ticker}'")
            price_analysis = str(self.price_agent(f"Analyze stock prices for {ticker}"))
            print(f"🔧 DEBUG: price_agent returned {len(price_analysis)} chars")
            
            print(f"🔧 DEBUG: Calling metrics_agent for ticker '{ticker}'")
            metrics_analysis = str(self.metrics_agent(f"Analyze financial metrics for {ticker}"))
            print(f"🔧 DEBUG: metrics_agent returned {len(metrics_analysis)} chars")
            
            print(f"🔧 DEBUG: Calling news_agent for ticker '{ticker}'")
            news_analysis = str(self.news_agent(f"Analyze recent news and sentiment for {ticker}"))
            print(f"🔧 DEBUG: news_agent returned {len(news_analysis)} chars")
            
            result = {
                "status": "success",
                "ticker": ticker,
                "company_info": company_info,
                "price_analysis": price_analysis,
                "metrics_analysis": metrics_analysis,
                "news_analysis": news_analysis,
                "coordination_method": "individual_agents"
            }
            print(f"🔧 DEBUG: _simple_analyze_company returning success result")
            return result
            
        except Exception as e:
            print(f"🔧 DEBUG: Exception in _simple_analyze_company: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"Individual agent analysis error: {str(e)}"}
    
    def _extract_ticker_from_info(self, company_info: str, query: str) -> str:
        """Extract ticker symbol from company information."""
        import re
        
        # First, check if the query itself is a ticker (most reliable)
        if re.match(r'^[A-Z]{1,5}$', query.upper().strip()):
            return query.upper().strip()
        
        # Look for specific ticker patterns in the company info
        ticker_patterns = [
            r'ticker[:\s]+([A-Z]{1,5})',
            r'symbol[:\s]+([A-Z]{1,5})',
            r'stock\s+symbol[:\s]+([A-Z]{1,5})',
            r'\(([A-Z]{1,5})\)',  # Ticker in parentheses like "Apple Inc (AAPL)"
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, company_info, re.IGNORECASE)
            if matches:
                ticker = matches[0].upper().strip()
                # Validate it's actually a ticker format
                if re.match(r'^[A-Z]{1,5}$', ticker):
                    return ticker
        
        # Try to extract from known company name patterns
        company_mappings = {
            'APPLE': 'AAPL',
            'MICROSOFT': 'MSFT', 
            'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN',
            'TESLA': 'TSLA',
            'NVIDIA': 'NVDA',
            'META': 'META'
        }
        
        query_upper = query.upper()
        for company, ticker in company_mappings.items():
            if company in query_upper:
                return ticker
        
        # Final fallback: if query looks like it could be a ticker, use it
        clean_query = re.sub(r'[^A-Z]', '', query.upper())
        if 1 <= len(clean_query) <= 5:
            return clean_query
            
        return query.upper().strip()  # Last resort


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
        print(f"🔧 DEBUG: analyze_company_tool called with query='{query}'")
        try:
            result = swarm_instance.analyze_company(query)
            print(f"🔧 DEBUG: swarm_instance.analyze_company returned: {type(result)}")
            if isinstance(result, dict) and result.get('status') == 'error':
                print(f"🔧 DEBUG: Error in swarm analysis: {result.get('message')}")
            return str(result)
        except Exception as e:
            print(f"🔧 DEBUG: Exception in analyze_company_tool: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    return Agent(
        system_prompt="""You are a stock analysis orchestrator. When a user asks you to analyze a company, you MUST extract the company name or ticker from their request and call analyze_company_tool with that parameter.

CRITICAL INSTRUCTIONS:
1. Extract the company name/ticker from the user's request (e.g., "AAPL", "Apple", "Microsoft", etc.)
2. Call analyze_company_tool(company_name) with the extracted company identifier
3. Only provide analysis based on the tool's response
4. Never generate fictional data

EXAMPLES:
- User: "Analyze AAPL" → Call: analyze_company_tool("AAPL")  
- User: "Investment analysis of Apple" → Call: analyze_company_tool("Apple")
- User: "Tell me about Microsoft stock" → Call: analyze_company_tool("Microsoft")""",
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
