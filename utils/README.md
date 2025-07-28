# Utils Directory

This directory contains utility scripts for debugging, diagnostics, and API analysis.

## Utility Files

### **API Diagnostics**
- `debug_finnhub.py` - Comprehensive Finnhub API testing and debugging
- `check_finnhub_plan.py` - Analyzes Finnhub plan features and limitations

## Usage

### **Debug Finnhub API Issues**
```bash
python utils/debug_finnhub.py
```
This script tests various Finnhub endpoints to identify:
- API key validity
- Available vs restricted endpoints
- Rate limiting behavior
- 403 Forbidden errors on historical data

### **Check Finnhub Plan Features**
```bash
python utils/check_finnhub_plan.py
```
This script determines your Finnhub plan tier by testing:
- Free tier features (quotes, company profiles)
- Paid tier features (historical candles, premium data)
- Rate limits and access restrictions

## Key Insights

### **Finnhub Free Tier Limitations**
Based on diagnostic results:
- ✅ **Available**: Real-time quotes, company profiles, basic metrics
- ❌ **Blocked**: Historical candle data (403 Forbidden)
- ⏱️ **Rate Limit**: 60 calls per minute

### **Why FMP Integration Was Needed**
The diagnostic utilities revealed that Finnhub's free tier blocks historical candle data, which led to implementing the hybrid approach:
- **Finnhub**: Real-time quotes and company data (free tier)
- **Financial Modeling Prep**: Historical OHLC data (250 calls/day free)

## Requirements

Both utilities require:
```bash
FINNHUB_API_KEY=your_finnhub_key_here
```

Optional for enhanced testing:
```bash
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here
```

## Expected Output

### **Working API Key**
```
✅ Found API key: d23ud81r01...
✅ Quote successful: {'c': 214.05, 'd': 0.17, ...}
✅ Profile successful: Apple Inc
❌ Historical Candles: 403 Forbidden (Expected on free tier)
```

### **Invalid/Missing API Key**
```
❌ FINNHUB_API_KEY not found in environment variables
Please add your Finnhub API key to a .env file
```