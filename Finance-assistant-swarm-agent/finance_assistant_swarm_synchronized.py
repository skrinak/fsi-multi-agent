#!/usr/bin/env python3
"""
Synchronized Finance Assistant Swarm Agent

A properly synchronized collaborative swarm of specialized agents for comprehensive stock analysis.
Uses Strands SDK proper synchronization mechanisms to avoid race conditions and formatting issues.
"""

# Standard library imports
import time
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# STRANDS AGENTS SDK (TOP PRIORITY)
from strands import Agent, tool
from strands.models import BedrockModel
from strands.multiagent import Swarm
from strands_tools import think, http_request

# Load environment variables - check multiple locations
load_dotenv()  # Current directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))  # Parent directory

# Third-party imports for ticker validation
import finnhub

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
    Validate ticker symbol using real-time quote API.
    
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
        
        # Initialize client for validation
        finnhub_client = finnhub.Client(api_key=api_key)
        
        # Test ticker with quote endpoint (real-time data)
        quote = finnhub_client.quote(ticker)
        
        # Check if quote contains valid data
        if not quote or 'c' not in quote:
            return {"valid": False, "error": f"No data found for ticker: {ticker}"}
        
        # API returns 0 for invalid tickers
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


@tool
def synchronized_report_builder(analysis_data: Dict[str, Any]) -> str:
    """
    Build a synchronized, properly formatted financial analysis report.
    
    This tool ensures all agent contributions are properly coordinated and formatted
    without race conditions or truncated messages.
    
    Args:
        analysis_data: Dictionary containing all agent analysis results
        
    Returns:
        Properly formatted comprehensive financial report
    """
    try:
        ticker = analysis_data.get("ticker", "Unknown")
        
        # Build report with proper synchronization
        report_sections = []
        
        # Header
        report_sections.append(f"📊 COMPREHENSIVE FINANCIAL ANALYSIS: {ticker}")
        report_sections.append("=" * 80)
        
        # Company Information Section
        if "company_info" in analysis_data:
            company_data = analysis_data["company_info"]
            report_sections.append("\n🏢 COMPANY OVERVIEW")
            report_sections.append("-" * 40)
            if isinstance(company_data, dict) and "data" in company_data:
                data = company_data["data"]
                report_sections.append(f"Company Name: {data.get('company_name', 'N/A')}")
                report_sections.append(f"Sector: {data.get('sector', 'N/A')}")
                report_sections.append(f"Market Cap: ${data.get('market_cap', 'N/A'):,}" if data.get('market_cap') != 'N/A' else "Market Cap: N/A")
                report_sections.append(f"Exchange: {data.get('exchange', 'N/A')}")
                
                if data.get('description'):
                    desc = data['description'][:500] + "..." if len(data.get('description', '')) > 500 else data.get('description', '')
                    report_sections.append(f"Business Description: {desc}")
        
        # Stock Price Analysis Section
        if "price_analysis" in analysis_data:
            price_data = analysis_data["price_analysis"]
            report_sections.append("\n📈 STOCK PRICE ANALYSIS")
            report_sections.append("-" * 40)
            if isinstance(price_data, dict) and "data" in price_data:
                data = price_data["data"]
                report_sections.append(f"Current Price: ${data.get('current_price', 'N/A')}")
                report_sections.append(f"Daily Change: {data.get('daily_change', 'N/A')}%")
                report_sections.append(f"Daily High: ${data.get('daily_high', 'N/A')}")
                report_sections.append(f"Daily Low: ${data.get('daily_low', 'N/A')}")
                report_sections.append(f"Previous Close: ${data.get('previous_close', 'N/A')}")
        
        # Financial Metrics Section
        if "financial_metrics" in analysis_data:
            metrics_data = analysis_data["financial_metrics"]
            report_sections.append("\n💰 FINANCIAL METRICS")
            report_sections.append("-" * 40)
            if isinstance(metrics_data, dict) and "data" in metrics_data:
                data = metrics_data["data"]
                
                # Valuation Metrics
                report_sections.append("Valuation Ratios:")
                report_sections.append(f"  • P/E Ratio: {data.get('pe_ratio', 'N/A')}")
                report_sections.append(f"  • Price-to-Book: {data.get('price_to_book', 'N/A')}")
                report_sections.append(f"  • Price-to-Sales: {data.get('price_to_sales', 'N/A')}")
                
                # Profitability Metrics
                report_sections.append("Profitability:")
                report_sections.append(f"  • Profit Margin: {data.get('profit_margins', 'N/A')}%")
                report_sections.append(f"  • ROE: {data.get('return_on_equity', 'N/A')}%")
                report_sections.append(f"  • ROA: {data.get('return_on_assets', 'N/A')}%")
                
                # Growth Metrics
                report_sections.append("Growth:")
                report_sections.append(f"  • Revenue Growth: {data.get('revenue_growth', 'N/A')}%")
                report_sections.append(f"  • Earnings Growth: {data.get('earnings_growth', 'N/A')}%")
        
        # News and Sentiment Section
        if "news_analysis" in analysis_data:
            news_data = analysis_data["news_analysis"]
            report_sections.append("\n📰 NEWS & MARKET SENTIMENT")
            report_sections.append("-" * 40)
            if isinstance(news_data, dict) and "data" in news_data:
                data = news_data["data"]
                recent_news = data.get("recent_news", [])
                if recent_news:
                    report_sections.append(f"Recent News Coverage: {len(recent_news)} articles found")
                    for i, news_item in enumerate(recent_news[:3], 1):  # Top 3 news items
                        report_sections.append(f"  {i}. {news_item.get('title', 'No title')}")
                        if news_item.get('source'):
                            report_sections.append(f"     Source: {news_item['source']}")
        
        # Investment Summary Section
        report_sections.append("\n🎯 INVESTMENT SUMMARY")
        report_sections.append("-" * 40)
        
        # Generate investment insights based on available data
        insights = []
        if "financial_metrics" in analysis_data:
            metrics = analysis_data["financial_metrics"]
            if isinstance(metrics, dict) and "data" in metrics:
                data = metrics["data"]
                pe_ratio = data.get('pe_ratio')
                if pe_ratio != 'N/A' and isinstance(pe_ratio, (int, float)):
                    if pe_ratio < 15:
                        insights.append("• Potentially undervalued based on P/E ratio")
                    elif pe_ratio > 25:
                        insights.append("• High P/E ratio may indicate growth expectations or overvaluation")
                
                profit_margin = data.get('profit_margins')
                if profit_margin != 'N/A' and isinstance(profit_margin, (int, float)):
                    if profit_margin > 20:
                        insights.append("• Strong profitability margins")
                    elif profit_margin < 5:
                        insights.append("• Low profit margins may indicate operational challenges")
        
        if insights:
            report_sections.extend(insights)
        else:
            report_sections.append("• Analysis requires more comprehensive data for detailed insights")
        
        # Data Attribution Footer
        report_sections.append("\n" + "=" * 80)
        report_sections.append("📊 Data Sources:")
        report_sections.append("• Historical Financial Data: Financial Modeling Prep API")  
        report_sections.append("• Real-time Quotes: Multi-Agent Systems APIs")
        report_sections.append("• Company Intelligence: Multi-source analysis with web intelligence")
        report_sections.append(f"• Report Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Join all sections with proper formatting
        final_report = "\n".join(report_sections)
        
        return final_report
        
    except Exception as e:
        return f"Error generating synchronized report: {str(e)}"


class SynchronizedStockAnalysisSwarm:
    """A properly synchronized collaborative swarm of specialized agents using Strands SDK."""

    def __init__(self):
        """Initialize the synchronized swarm with proper coordination mechanisms."""
        # Check for API key
        if not os.getenv('FINNHUB_API_KEY'):
            print("⚠️ Warning: FINNHUB_API_KEY not found in environment variables")
            print("Please add your API key to a .env file for full functionality")
        
        # Create specialized agents for swarm
        self._create_specialized_agents()
        
        # Initialize Swarm with proper synchronization using Strands SDK
        self.swarm = Swarm(
            nodes=[
                self.company_info_agent,
                self.price_analysis_agent, 
                self.metrics_analysis_agent,
                self.news_analysis_agent,
                self.report_coordinator_agent
            ],
            max_handoffs=10,
            max_iterations=15,
            execution_timeout=300.0,
            node_timeout=60.0
        )
        
        print("✅ Synchronized Finance Assistant Swarm initialized with proper coordination")
    
    def _create_specialized_agents(self):
        """Create specialized agents with clear roles and handoff coordination."""
        
        # Company Information Specialist
        self.company_info_agent = Agent(
            name="company_info_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Company Information Specialist in a synchronized financial analysis swarm.

CRITICAL SYNCHRONIZATION RULES:
1. Store all results in shared_context for other agents
2. Use structured data formats for consistency  
3. Hand off to the next agent after completing your analysis
4. Wait for coordination signals before proceeding

Your role: Gather comprehensive company information using available APIs.
- Use get_company_info to fetch company profile and business details
- Store results as 'company_info' in shared context
- Hand off to price analysis agent when complete

Always format your output as structured data that other agents can use.""",
            tools=[get_company_info],
        )
        
        # Stock Price Analysis Specialist  
        self.price_analysis_agent = Agent(
            name="price_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Stock Price Analysis Specialist in a synchronized financial analysis swarm.

CRITICAL SYNCHRONIZATION RULES:
1. Read ticker from shared_context set by company info agent
2. Store your analysis as 'price_analysis' in shared context
3. Use structured data formats for consistency
4. Hand off to metrics analysis agent when complete

Your role: Analyze stock price data, trends, and trading patterns.
- Use get_stock_prices to fetch current and historical price data
- Focus on price movements, volatility, and technical indicators
- Store results in structured format for other agents

Wait for company_info completion before starting your analysis.""",
            tools=[get_stock_prices],
        )
        
        # Financial Metrics Analysis Specialist
        self.metrics_analysis_agent = Agent(
            name="metrics_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Financial Metrics Analysis Specialist in a synchronized financial analysis swarm.

CRITICAL SYNCHRONIZATION RULES:
1. Read ticker from shared_context set by previous agents
2. Store your analysis as 'financial_metrics' in shared context  
3. Use structured data formats for consistency
4. Hand off to news analysis agent when complete

Your role: Analyze financial ratios, profitability, and fundamental metrics.
- Use get_financial_metrics to fetch comprehensive financial data
- Focus on valuation, growth, profitability, and financial health
- Store results in structured format for other agents

Coordinate with previous agents' findings for comprehensive analysis.""",
            tools=[get_financial_metrics],
        )
        
        # News and Sentiment Analysis Specialist
        self.news_analysis_agent = Agent(
            name="news_analysis_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a News and Sentiment Analysis Specialist in a synchronized financial analysis swarm.

CRITICAL SYNCHRONIZATION RULES:
1. Read ticker from shared_context set by previous agents
2. Store your analysis as 'news_analysis' in shared context
3. Use structured data formats for consistency  
4. Hand off to report coordinator when complete

Your role: Analyze recent news and market sentiment.
- Use get_stock_news to fetch recent company news and developments
- Focus on sentiment analysis and impact on investment outlook
- Store results in structured format for final report

Wait for previous agents to complete before starting your analysis.""",
            tools=[get_stock_news],
        )
        
        # Report Coordination Agent
        self.report_coordinator_agent = Agent(
            name="report_coordinator",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are the Report Coordinator in a synchronized financial analysis swarm.

CRITICAL SYNCHRONIZATION RULES:
1. Wait for ALL other agents to complete their analysis
2. Read all analysis data from shared_context
3. Use synchronized_report_builder tool to create final report
4. Ensure no data races or formatting conflicts

Your role: Coordinate and synthesize all agent analyses into a comprehensive report.
- Gather all results from shared_context
- Use synchronized_report_builder to create the final formatted report
- Ensure professional formatting and consistency
- Provide clear investment insights based on all agent contributions

NEVER generate a report until all other agents have completed their work.""",
            tools=[synchronized_report_builder],
        )

    def analyze_company(self, query: str) -> Dict[str, Any]:
        """
        Run synchronized swarm analysis for a company.
        
        Args:
            query: Company name or ticker symbol to analyze
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        try:
            print(f"\n🔍 Starting synchronized swarm analysis for: {query}")
            print("=" * 60)
            
            # Validate ticker if it looks like one
            import re
            if re.match(r'^[A-Z]{1,5}$', query.upper()):
                validation = validate_ticker(query)
                if not validation["valid"]:
                    return {"status": "error", "message": validation["error"]}
                print(f"✅ Ticker validated: {validation['message']}")
            
            # Initialize shared context with the query
            task_prompt = f"""Conduct comprehensive financial analysis for: {query}

COORDINATION PROTOCOL:
1. Company Info Agent: Fetch company details and store in shared_context
2. Price Analysis Agent: Analyze stock prices using ticker from shared_context  
3. Metrics Analysis Agent: Analyze financial metrics using ticker from shared_context
4. News Analysis Agent: Analyze recent news using ticker from shared_context
5. Report Coordinator: Synthesize all analyses into final formatted report

Each agent must complete their work and store results in shared_context before the next agent begins.
Use proper handoff coordination to prevent race conditions and ensure data synchronization.

Query: {query}"""
            
            # Execute swarm with proper synchronization
            print("🚀 Executing synchronized swarm analysis...")
            result = self.swarm(task_prompt)
            
            print("✅ Swarm analysis completed successfully")
            
            # Extract the final report from the swarm result
            if hasattr(result, 'content') and result.content:
                final_content = str(result.content)
                return {
                    "status": "success",
                    "query": query,
                    "analysis_report": final_content,
                    "coordination_method": "synchronized_swarm",
                    "execution_time": getattr(result, 'execution_time', 0),
                    "agents_involved": 5
                }
            else:
                return {
                    "status": "error", 
                    "message": "Swarm analysis completed but no content was generated"
                }
                
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Synchronized swarm analysis failed: {str(e)}"
            }

    def _extract_ticker_from_info(self, company_info: str, query: str) -> str:
        """Extract ticker symbol from company information with fallback logic."""
        import re
        
        # First, check if the query itself is a ticker (most reliable)
        if re.match(r'^[A-Z]{1,5}$', query.upper().strip()):
            return query.upper().strip()
        
        # Look for specific ticker patterns in the company info
        ticker_patterns = [
            r'ticker[:\s]+([A-Z]{1,5})',
            r'symbol[:\s]+([A-Z]{1,5})',  
            r'stock\s+symbol[:\s]+([A-Z]{1,5})',
            r'\(([A-Z]{1,5})\)',  # Ticker in parentheses
        ]
        
        for pattern in ticker_patterns:
            matches = re.findall(pattern, company_info, re.IGNORECASE)
            if matches:
                ticker = matches[0].upper().strip()
                if re.match(r'^[A-Z]{1,5}$', ticker):
                    return ticker
        
        # Try known company mappings  
        company_mappings = {
            'APPLE': 'AAPL', 'MICROSOFT': 'MSFT', 'GOOGLE': 'GOOGL',
            'AMAZON': 'AMZN', 'TESLA': 'TSLA', 'NVIDIA': 'NVDA', 'META': 'META'
        }
        
        query_upper = query.upper()
        for company, ticker in company_mappings.items():
            if company in query_upper:
                return ticker
        
        # Final fallback
        clean_query = re.sub(r'[^A-Z]', '', query.upper())
        if 1 <= len(clean_query) <= 5:
            return clean_query
            
        return query.upper().strip()


def create_synchronized_orchestration_agent() -> Agent:
    """Create the main orchestration agent that coordinates the synchronized swarm."""
    if not os.getenv('FINNHUB_API_KEY'):
        print("⚠️ Warning: FINNHUB_API_KEY not found - some features may be limited")
    
    swarm_instance = SynchronizedStockAnalysisSwarm()
    
    @tool
    def analyze_company_synchronized(query: str) -> str:
        """Analyze a company using the synchronized swarm of financial agents."""
        try:
            result = swarm_instance.analyze_company(query)
            if result["status"] == "success":
                return result["analysis_report"]
            else:
                return f"Analysis failed: {result.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Synchronized analysis error: {str(e)}"
    
    return Agent(
        system_prompt="""You are a synchronized stock analysis orchestrator using properly coordinated multi-agent systems.

CRITICAL INSTRUCTIONS:
1. Extract company name/ticker from user requests
2. Call analyze_company_synchronized(company_identifier) 
3. Return the synchronized report exactly as provided
4. Never generate additional analysis - use only the coordinated swarm results

SYNCHRONIZATION BENEFITS:
- No race conditions or truncated messages
- Properly formatted reports with consistent structure  
- Coordinated agent handoffs prevent data corruption
- Professional-grade output suitable for investment decisions

EXAMPLES:
- User: "Analyze AAPL" → Call: analyze_company_synchronized("AAPL")  
- User: "Investment analysis of Apple" → Call: analyze_company_synchronized("Apple")
- User: "Tell me about Microsoft stock" → Call: analyze_company_synchronized("Microsoft")""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
        tools=[analyze_company_synchronized],
    )


def create_initial_messages() -> List[Dict]:
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "Hello, I need synchronized financial analysis."}],
        },
        {
            "role": "assistant", 
            "content": [
                {
                    "text": "I'm ready to provide synchronized financial analysis using coordinated multi-agent systems. Please provide a company name or ticker for comprehensive analysis."
                }
            ],
        },
    ]


def main():
    """Main function to run the synchronized finance assistant swarm."""
    # Check for API key at startup
    if not os.getenv('FINNHUB_API_KEY'):
        print("❌ Error: FINNHUB_API_KEY not found in environment variables")
        print("Please add your API key to a .env file:")
        print("FINNHUB_API_KEY=your_api_key_here")
        print("\nRunning in limited mode...\n")
    
    # Create the synchronized orchestration agent
    orchestration_agent = create_synchronized_orchestration_agent()
    orchestration_agent.messages = create_initial_messages()

    print("\n🏢 Synchronized Stock Analysis Swarm 📊")
    print("=" * 60)
    print("Professional investment analysis with coordinated multi-agent systems")
    print("✅ No race conditions • ✅ Proper formatting • ✅ Synchronized reports")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Company to analyze> ").strip()

        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy investing!")
            break
            
        if not query.strip():
            print("Please enter a company name or ticker symbol.")
            continue

        print(f"\n🔍 Initiating synchronized analysis for {query.upper()}...")
        print("-" * 60)

        try:
            # Create the user message
            user_message = {
                "role": "user",
                "content": [
                    {
                        "text": f"Please conduct synchronized comprehensive investment analysis of {query} using coordinated multi-agent systems."
                    }
                ],
            }

            # Add message to conversation
            orchestration_agent.messages.append(user_message)

            # Get synchronized response  
            response = orchestration_agent(user_message["content"][0]["text"])

            # Display synchronized results
            print(f"\n📊 Synchronized Investment Analysis for {query.upper()}:")
            print("=" * 80)
            print(f"{response}")
            print("\n" + "=" * 80)

        except Exception as e:
            print(f"❌ Error in synchronized analysis for {query}: {str(e)}\n")
            
            if "FINNHUB_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid API key")
                break
            elif "ThrottlingException" in str(e):
                print("⏱️ Rate limit reached. Waiting 5 seconds...")
                time.sleep(5)
                continue
        finally:
            # Reset conversation after each query 
            orchestration_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()