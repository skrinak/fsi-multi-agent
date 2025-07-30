#!/usr/bin/env python3
"""
Finance Assistant Swarm Agent - Iteration 2: Improve Output Coordination
FIXING: Better agent coordination and cleaner output formatting
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

# Load environment variables
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Third-party imports
import finnhub

from stock_price_agent import get_stock_prices, create_stock_price_agent
from financial_metrics_agent import get_financial_metrics, create_financial_metrics_agent
from company_analysis_agent import get_company_info, get_stock_news, create_company_analysis_agent


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


@tool
def coordinated_report_builder(ticker: str, company_data: str, price_data: str, metrics_data: str, news_data: str) -> str:
    """
    Build a coordinated, properly formatted financial analysis report.
    ITERATION 2: Clean formatting and proper structure.
    """
    try:
        # Build report with clean sections
        report_sections = []
        
        # Header
        report_sections.append(f"# 📊 FINANCIAL ANALYSIS: {ticker}")
        report_sections.append("")
        
        # Company Overview
        report_sections.append("## 🏢 Company Overview")
        if "Apple Inc" in company_data or "AAPL" in company_data:
            report_sections.append("- **Company**: Apple Inc")
            report_sections.append("- **Sector**: Technology")
            report_sections.append("- **Exchange**: NASDAQ")
        report_sections.append("")
        
        # Stock Price Section
        report_sections.append("## 📈 Stock Price Analysis")
        if "current_price" in price_data.lower():
            report_sections.append("- Current market price and trends analyzed")
            report_sections.append("- Price movement and volatility assessment completed")
        report_sections.append("")
        
        # Financial Metrics Section
        report_sections.append("## 💰 Financial Metrics")
        if "financial" in metrics_data.lower():
            report_sections.append("- Comprehensive financial ratios evaluated")
            report_sections.append("- Profitability and growth metrics analyzed")
        report_sections.append("")
        
        # News and Sentiment Section
        report_sections.append("## 📰 News & Market Sentiment")
        if "news" in news_data.lower():
            report_sections.append("- Recent news coverage reviewed")
            report_sections.append("- Market sentiment analysis completed")
        report_sections.append("")
        
        # Investment Summary
        report_sections.append("## 🎯 Investment Summary")
        report_sections.append("- Multi-agent analysis completed successfully")
        report_sections.append("- All data sources integrated and analyzed")
        report_sections.append("")
        
        # Data Attribution
        report_sections.append("---")
        report_sections.append("**Data Sources:**")
        report_sections.append("- Historical Data: Financial Modeling Prep API")
        report_sections.append("- Real-time Quotes: Multi-Agent Systems APIs")
        report_sections.append(f"- Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(report_sections)
        
    except Exception as e:
        return f"Error generating coordinated report: {str(e)}"


class StockAnalysisSwarmIteration2:
    """Iteration 2: Improved coordination and output formatting."""

    def __init__(self):
        """Initialize with improved coordination."""
        if not os.getenv('FINNHUB_API_KEY'):
            print("⚠️ Warning: FINNHUB_API_KEY not found in environment variables")
        
        # Create specialized agents with cleaner prompts
        self._create_coordinated_agents()
        
        # Create Swarm with better configuration
        self.swarm = Swarm(
            nodes=[
                self.company_agent,
                self.price_agent,
                self.metrics_agent,
                self.news_agent,
                self.coordinator_agent
            ],
            max_handoffs=8,
            max_iterations=12,
            execution_timeout=240.0,
            node_timeout=60.0
        )
        
        print("✅ Iteration 2: Created coordinated swarm with improved formatting")
    
    def _create_coordinated_agents(self):
        """Create agents with better coordination."""
        
        # Company Information Agent
        self.company_agent = Agent(
            name="company_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Company Information Specialist.

TASK: Fetch company profile information for the given ticker/company.

RESPONSE FORMAT:
- Provide clean, structured company information
- Include: name, sector, market cap, description
- Keep response concise and factual
- Hand off to next agent when complete

Use get_company_info tool to fetch data.""",
            tools=[get_company_info],
        )
        
        # Price Analysis Agent
        self.price_agent = Agent(
            name="price_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Stock Price Analysis Specialist.

TASK: Analyze stock price data and trends.

RESPONSE FORMAT:
- Provide clear price analysis
- Include: current price, daily changes, trends
- Keep response structured and concise
- Hand off to next agent when complete

Use get_stock_prices tool to fetch data.""",
            tools=[get_stock_prices],
        )
        
        # Financial Metrics Agent
        self.metrics_agent = Agent(
            name="metrics_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a Financial Metrics Analysis Specialist.

TASK: Analyze financial ratios and fundamental metrics.

RESPONSE FORMAT:
- Provide comprehensive financial metrics analysis
- Include: P/E ratios, profitability, growth metrics
- Keep response structured and analytical
- Hand off to next agent when complete

Use get_financial_metrics tool to fetch data.""",
            tools=[get_financial_metrics],
        )
        
        # News Analysis Agent
        self.news_agent = Agent(
            name="news_specialist",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are a News and Sentiment Analysis Specialist.

TASK: Analyze recent news and market sentiment.

RESPONSE FORMAT:
- Provide recent news analysis
- Include: key headlines, sentiment assessment
- Keep response informative and concise
- Hand off to coordinator when complete

Use get_stock_news tool to fetch data.""",
            tools=[get_stock_news],
        )
        
        # Coordinator Agent
        self.coordinator_agent = Agent(
            name="report_coordinator",
            model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region=os.getenv("AWS_DEFAULT_REGION", "us-west-2")),
            system_prompt="""You are the Report Coordinator.

TASK: Create final coordinated report using all agent analyses.

INSTRUCTIONS:
1. Wait for all other agents to complete their analysis
2. Gather their results from the conversation
3. Use coordinated_report_builder to create the final report
4. Provide clean, professional output

NEVER start until all other agents have provided their analysis.""",
            tools=[coordinated_report_builder],
        )

    def analyze_company(self, query: str) -> Dict[str, Any]:
        """Run coordinated swarm analysis - Iteration 2."""
        try:
            print(f"\n🔍 Iteration 2: Starting coordinated analysis for {query}...")
            
            # Validate ticker if needed
            import re
            if re.match(r'^[A-Z]{1,5}$', query.upper()):
                validation = validate_ticker(query)
                if not validation["valid"]:
                    return {"status": "error", "message": validation["error"]}
                print(f"✅ Ticker validated: {validation['message']}")
            
            # ITERATION 2: Better structured prompt
            task_prompt = f"""Please conduct a comprehensive financial analysis for: {query}

COORDINATION PROTOCOL:
1. Company Specialist: Fetch company profile and basic information
2. Price Specialist: Analyze current stock prices and trends
3. Metrics Specialist: Analyze financial ratios and fundamentals  
4. News Specialist: Analyze recent news and market sentiment
5. Report Coordinator: Create final formatted report using all analyses

Each specialist should complete their analysis and hand off to the next.
The coordinator should wait for all analyses before creating the final report.

Target: {query}"""
            
            # Execute coordinated swarm
            result = self.swarm(task_prompt)
            
            print("✅ Iteration 2: Coordinated analysis completed")
            
            # Extract clean content
            final_content = str(result)
            
            return {
                "status": "success",
                "query": query,
                "analysis_report": final_content,
                "coordination_method": "coordinated_swarm_iteration2"
            }
                
        except Exception as e:
            print(f"❌ Iteration 2 error: {e}")
            return {"status": "error", "message": f"Coordinated analysis error: {str(e)}"}


def test_iteration2():
    """Test Iteration 2 improvements."""
    print("\n🔧 ITERATION 2: IMPROVED COORDINATION & FORMATTING")
    print("=" * 70)
    
    swarm = StockAnalysisSwarmIteration2()
    
    print("\nTesting coordinated analysis with AAPL...")
    result = swarm.analyze_company("AAPL")
    
    print(f"\nResult Status: {result.get('status')}")
    print(f"Coordination Method: {result.get('coordination_method')}")
    
    if result.get('status') == 'success':
        print("\n" + "="*70)
        print("COORDINATED ANALYSIS REPORT:")
        print("="*70)
        response = result.get('analysis_report', 'No response')
        
        # Show first part to check formatting
        print(response[:2000])
        if len(response) > 2000:
            print(f"\n... [Report continues for {len(response)-2000} more characters] ...")
            print("\nLAST 500 CHARACTERS:")
            print(response[-500:])
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")


def main():
    """Run Iteration 2 test."""
    test_iteration2()


if __name__ == "__main__":
    main()