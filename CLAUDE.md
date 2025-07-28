# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a comprehensive multi-agent systems implementation for Financial Services Intelligence (FSI) applications. **All implementations have been migrated from yfinance to Finnhub API and converted from Jupyter notebooks to executable Python modules.**

### Migration Status: COMPLETE ✅
- **All 12 files successfully processed** in sequential order
- **Complete yfinance → finnhub API migration** for all financial agents
- **All Jupyter notebooks converted to Python modules** with enhanced functionality
- **Production-ready codebase** with comprehensive error handling and API validation

## Repository Structure

### Core Financial Agent Components

- **Finance-assistant-swarm-agent/**: Complete finance agent swarm with Finnhub integration
  - `finance_assistant_swarm.py`: Main orchestrator with swarm coordination
  - `stock_price_agent.py`: Real-time stock data via Finnhub API
  - `financial_metrics_agent.py`: Comprehensive financial metrics analysis
  - `company_analysis_agent.py`: Company research with multi-source intelligence
  - `SwarmAgentArchitectureDescription.py`: Architecture documentation module

### Multi-Agent Pattern Implementations  

- **swarm/**: Collaborative agent patterns and mesh architectures
  - `swarm.py`: Basic swarm concepts and shared memory systems
  - `Swarm-DemandLetters.py`: Legal document analysis with competitive/collaborative patterns
  - `FinancialResearch_MeshSwarm.py`: Mesh swarm financial analysis system

- **graph_IntelligentLoanUnderwriting/**: Hierarchical loan underwriting system
  - `graph.py`: Agent graph topology fundamentals and examples
  - `IntelligentLoanApplication_Graph.py`: Complete loan underwriting workflow

- **WorkFlow_ClaimsAdjudication/**: Sequential claims processing workflow
  - `ClaimsAdjudication_SequentialPattern.py`: Autonomous claims adjudication system

## Development Environment

### Required Environment Variables

**CRITICAL**: All financial agents require Finnhub API key:

```bash
# .env file (required)
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### Dependencies

The project uses different dependency management approaches:

1. **Finance-assistant-swarm-agent**: Uses `pyproject.toml` with uv package manager
2. **Other modules**: Use `requirements.txt` files

### Core Dependencies

All modules depend on:
- `strands`: Core agent framework (Strands Agents SDK)
- `strands-agents-tools`: Agent tooling and utilities

Finance agent additionally uses:
- `finnhub-python>=2.4.18`: Stock market and financial data via Finnhub API (**replaces yfinance**)
- `python-dotenv>=1.0.0`: Environment variable management
- `pandas`: Data manipulation and analysis
- `boto3`: AWS Bedrock integration for LLM models
- `requests`: HTTP requests for web scraping
- `beautifulsoup4`: HTML parsing for web intelligence

Document processing modules use:
- `PyPDF2`: PDF document extraction for loan applications and legal documents

### Installation Commands

For Finance-assistant-swarm-agent:
```bash
cd Finance-assistant-swarm-agent
uv sync
```

For other modules:
```bash
cd [module-directory]
pip install -r requirements.txt
```

## Running the System

### Main Entry Points

**1. Finance Assistant Swarm (Primary System)**
```bash
cd Finance-assistant-swarm-agent
python finance_assistant_swarm.py
```

**2. Individual Agents (Direct Execution)**
```bash
cd Finance-assistant-swarm-agent
python stock_price_agent.py          # Stock price analysis with Finnhub
python financial_metrics_agent.py    # Financial metrics analysis
python company_analysis_agent.py     # Company research and analysis
```

**3. Multi-Agent Pattern Demonstrations**
```bash
python swarm/FinancialResearch_MeshSwarm.py                        # Mesh swarm research
python graph_IntelligentLoanUnderwriting/IntelligentLoanApplication_Graph.py  # Loan underwriting
python WorkFlow_ClaimsAdjudication/ClaimsAdjudication_SequentialPattern.py    # Claims processing
```

### Programmatic Usage

**Finance Assistant Swarm:**
```python
from finance_assistant_swarm import StockAnalysisSwarm, create_orchestration_agent

# Use swarm system
swarm = StockAnalysisSwarm()
result = swarm.analyze_company("AAPL")

# Use orchestration agent
agent = create_orchestration_agent()
response = agent("Provide comprehensive analysis of Apple Inc")
```

**Individual Finnhub-Powered Agents:**
```python
from stock_price_agent import get_stock_prices, create_stock_price_agent
from financial_metrics_agent import get_financial_metrics
from company_analysis_agent import get_company_info, get_stock_news

# Direct tool usage (requires FINNHUB_API_KEY)
price_data = get_stock_prices("AAPL")
metrics = get_financial_metrics("AAPL") 
company_info = get_company_info("AAPL")
news = get_stock_news("AAPL")

# Agent usage for conversational interface
price_agent = create_stock_price_agent()
response = price_agent("Analyze AAPL stock price trends over the last 3 months")
```

## Architecture Patterns

### 1. Sequential Workflow (Claims Adjudication)
- Each agent completes tasks before passing to next agent
- Clear dependencies and state management
- Used for compliance-heavy processes

### 2. Hierarchical Graph (Loan Underwriting)  
- Centralized coordination with specialized roles
- Executive-manager-specialist delegation patterns
- Clear chains of command and responsibility

### 3. Mesh Swarm (Financial Research)
- Direct agent-to-agent communication
- Collaborative reasoning and emergent intelligence
- Shared memory for distributed problem solving

## Key Implementation Patterns

### Agent Creation (Post-Migration)
All agents follow the updated pattern:
1. Tool creation with `@tool` decorators from Strands SDK
2. **Finnhub API integration** with comprehensive error handling
3. Environment variable management with `python-dotenv`
4. Structured data processing with confidence scoring
5. Multi-source intelligence (Finnhub + web scraping)
6. Professional-grade financial analysis output

### Swarm Coordination
- Uses `Swarm` class with shared memory systems
- `SwarmAgent` instances for specialized financial roles
- Coordination patterns: "collaborative", "competitive", "mesh", "hierarchical", "sequential"
- Fallback to individual agent coordination when swarm tools unavailable

### Data Flow and API Integration
- **Primary Data Source**: Finnhub API for all financial data
- **Secondary Sources**: Web scraping for enhanced company intelligence  
- **Error Handling**: Comprehensive API key validation and rate limiting
- **Shared Memory**: Complete context sharing across agent networks
- **Fallback Mechanisms**: Graceful degradation when external APIs unavailable

## Testing and Development

### No Automated Testing
The repository does not contain automated test suites. Testing is done through Python module execution and manual verification.

### Development Workflow
1. Modify agent implementations in `.py` files
2. Test changes by running Python modules directly
3. Verify multi-agent coordination through swarm execution
4. Check integration with external APIs (Finnhub, web scraping)

### Environment Setup (Updated Post-Migration)
1. **REQUIRED**: Create `.env` file with `FINNHUB_API_KEY=your_api_key`
2. Install dependencies with `uv sync` (finance agents) or `pip install -r requirements.txt`
3. Test Finnhub connectivity: `python -c "from stock_price_agent import get_stock_prices; print(get_stock_prices('AAPL'))"`
4. Verify all Python modules execute without errors

## External Integrations

### APIs Used (Post-Migration)
- **Finnhub (Primary)**: Complete financial data ecosystem via finnhub-python>=2.4.18
  - Real-time stock quotes and historical data
  - Company profiles and financial metrics  
  - Company news and market intelligence
- **Web Scraping (Secondary)**: Enhanced company intelligence via requests/BeautifulSoup
  - Company websites for additional context
  - Multiple news sources (MarketWatch, CNBC, Seeking Alpha, Google News)
- **AWS Bedrock**: LLM model integration via boto3

### Data Sources
- **Real-time Financial Data**: Finnhub API (replaces all yfinance functionality)
- **Enhanced Company Intelligence**: Multi-source web scraping with fallback mechanisms
- **Document Processing**: PDF extraction for loan applications, legal documents, financial statements
- **Structured Claims Data**: JSON format for FNOL and insurance claims processing

### Finnhub API Configuration
- **API Key**: Stored in `.env` file as `FINNHUB_API_KEY` (REQUIRED for all financial agents)
- **Rate Limits**: 60 calls/minute on free tier (built-in rate limiting and error handling)
- **Primary Endpoints**:
  - `/quote` - Real-time stock quotes with daily changes
  - `/stock/candle` - Historical OHLCV data with timestamp conversion
  - `/stock/company-profile2` - Comprehensive company information  
  - `/stock/metric` - Financial ratios and fundamental metrics
  - `/company-news` - Company-specific news and developments

### Migration Notes
- **yfinance Completely Removed**: All ticker.history(), ticker.info, ticker.news replaced
- **Enhanced Error Handling**: Comprehensive API validation and fallback mechanisms
- **Improved Data Quality**: Institutional-grade data from Finnhub vs consumer-grade yfinance
- **Rate Limiting**: Built-in handling for API quotas and throttling

## Security Considerations

This is a research/educational repository focused on defensive AI applications. All implementations demonstrate:
- Secure API integration patterns
- Error handling for external data sources
- Controlled agent autonomy with human oversight capabilities
- No storage of sensitive financial data or credentials