# Test Directory

This directory contains test scripts for validating the FSI-MAS multi-agent system functionality.

## Test Files

### **Core Functionality Tests**
- `simple_test.py` - Basic test of stock_price_agent get_stock_prices function
- `test_multiple_stocks.py` - Multi-stock testing for robustness validation
- `test_agent_function.py` - Test agent function with proper environment setup

### **API Integration Tests**
- `test_fmp_direct.py` - Direct Financial Modeling Prep API testing
- `test_fmp_integration.py` - Full FMP integration testing with stock_price_agent
- `test_dotenv.py` - Environment variable loading validation

## Running Tests

### **Prerequisites**
Ensure you have the required API keys in your `.env` file:
```bash
FINNHUB_API_KEY=your_finnhub_key_here
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here
```

### **Run Individual Tests**
```bash
# From the Finance-assistant-swarm-agent directory
cd ../Finance-assistant-swarm-agent

# Test basic functionality
uv run python ../test/simple_test.py

# Test multiple stocks
uv run python ../test/test_multiple_stocks.py

# Test FMP API directly
python ../test/test_fmp_direct.py

# Test environment loading
python ../test/test_dotenv.py
```

### **Expected Results**
All tests should pass when:
- API keys are properly configured
- Network connectivity is available
- API rate limits are not exceeded

## Test Coverage

- ✅ **Stock Price Agent**: Basic functionality and multi-stock testing
- ✅ **FMP API Integration**: Direct API calls and hybrid integration
- ✅ **Environment Configuration**: .env loading and validation
- ✅ **Error Handling**: Missing API keys and invalid responses