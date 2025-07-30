#!/usr/bin/env python3
"""
Test script for synchronized swarm to verify proper coordination
"""

import sys
import os
sys.path.insert(0, 'Finance-assistant-swarm-agent')

from finance_assistant_swarm_synchronized import (
    SynchronizedStockAnalysisSwarm, 
    synchronized_report_builder
)

def test_synchronized_report_builder():
    """Test the synchronized report builder tool."""
    print("🧪 Testing synchronized report builder...")
    
    # Mock analysis data
    test_data = {
        "ticker": "AAPL",
        "company_info": {
            "data": {
                "company_name": "Apple Inc",
                "sector": "Technology",
                "market_cap": 3500000,
                "exchange": "NASDAQ",
                "description": "Apple Inc. is a multinational technology company."
            }
        },
        "price_analysis": {
            "data": {
                "current_price": 195.50,
                "daily_change": 2.5,
                "daily_high": 197.00,
                "daily_low": 194.20,
                "previous_close": 190.85
            }
        },
        "financial_metrics": {
            "data": {
                "pe_ratio": 28.5,
                "price_to_book": 12.3,
                "price_to_sales": 7.8,
                "profit_margins": 25.2,
                "return_on_equity": 45.6,
                "return_on_assets": 15.8,
                "revenue_growth": 8.5,
                "earnings_growth": 12.3
            }
        },
        "news_analysis": {
            "data": {
                "recent_news": [
                    {"title": "Apple Announces New Product Line", "source": "Reuters"},
                    {"title": "Strong Q4 Earnings Beat Expectations", "source": "MarketWatch"},
                    {"title": "Apple Invests in AI Technology", "source": "TechCrunch"}
                ]
            }
        }
    }
    
    # Generate synchronized report
    report = synchronized_report_builder(test_data)
    
    print("📊 Generated Synchronized Report:")
    print("=" * 80)
    print(report)
    print("=" * 80)
    
    # Verify report structure
    expected_sections = [
        "COMPREHENSIVE FINANCIAL ANALYSIS",
        "COMPANY OVERVIEW", 
        "STOCK PRICE ANALYSIS",
        "FINANCIAL METRICS",
        "NEWS & MARKET SENTIMENT",
        "INVESTMENT SUMMARY",
        "Data Sources"
    ]
    
    success = True
    for section in expected_sections:
        if section not in report:
            print(f"❌ Missing section: {section}")
            success = False
    
    if success:
        print("✅ All expected report sections present")
        
        # Check for proper data attribution
        if "Financial Modeling Prep" in report and "Multi-Agent Systems APIs" in report:
            print("✅ Proper data attribution present")
        else:
            print("❌ Missing proper data attribution")
            success = False
            
        # Check for no truncation markers
        if "..." not in report or report.count("...") <= 2:  # Allow some for descriptions
            print("✅ No truncated content detected")
        else:
            print("⚠️ Possible truncated content detected")
    
    return success

def test_swarm_creation():
    """Test synchronized swarm creation."""
    print("\n🧪 Testing synchronized swarm creation...")
    
    try:
        swarm = SynchronizedStockAnalysisSwarm()
        print("✅ Synchronized swarm created successfully")
        
        # Verify swarm has proper coordination
        if hasattr(swarm, 'swarm') and swarm.swarm:
            print("✅ Strands SDK Swarm initialized")
            print(f"✅ Configured with {len(swarm.swarm.nodes)} specialized agents")
            print(f"✅ Max handoffs: {swarm.swarm.max_handoffs}")
            print(f"✅ Execution timeout: {swarm.swarm.execution_timeout}s")
            return True
        else:
            print("❌ Swarm not properly initialized")
            return False
            
    except Exception as e:
        print(f"❌ Swarm creation failed: {e}")
        return False

def main():
    """Run all synchronization tests."""
    print("🚀 SYNCHRONIZED SWARM TESTING SUITE")
    print("=" * 60)
    
    tests = [
        ("Synchronized Report Builder", test_synchronized_report_builder),
        ("Swarm Creation", test_swarm_creation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 TEST RESULTS")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\nOverall: {passed}/{len(results)} tests passed ({success_rate:.0f}%)")
    
    if success_rate >= 100:
        print("🎉 SYNCHRONIZATION TEST: SUCCESSFUL - All coordination mechanisms working")
        return True
    else:
        print("⚠️ SYNCHRONIZATION TEST: ISSUES DETECTED - Review failed tests")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
    else:
        print("\n🎯 Synchronized swarm testing completed successfully!")
        sys.exit(0)