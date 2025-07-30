#!/usr/bin/env python3
"""
Quick validation test to confirm multi-agent systems are working properly.
"""

import sys
import os
import signal
from dotenv import load_dotenv

# Add the Finance-assistant-swarm-agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Finance-assistant-swarm-agent'))

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Test timed out")

def run_with_timeout(func, timeout_seconds=30):
    """Run a function with a timeout to prevent hanging."""
    if os.name == 'nt':  # Windows doesn't support alarm
        return func()
    
    # Set up the timeout
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    
    try:
        result = func()
        signal.alarm(0)  # Cancel the alarm
        return result
    except TimeoutError:
        print(f"⚠️ Test timed out after {timeout_seconds} seconds")
        return False
    finally:
        signal.signal(signal.SIGALRM, old_handler)

def test_finance_agent_creation():
    """Test that we can create and use a finance agent"""
    print("🧪 QUICK VALIDATION: Finance Agent Creation")
    print("=" * 50)
    
    load_dotenv()
    
    try:
        from stock_price_agent import create_stock_price_agent
        
        print("Creating stock price agent...")
        agent = create_stock_price_agent()
        print("✅ Stock price agent created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_hierarchical_system():
    """Test basic hierarchical system functionality"""
    print("\n🏗️ QUICK VALIDATION: Hierarchical System")
    print("=" * 50)
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'graph_IntelligentLoanUnderwriting'))
    
    system = None
    try:
        from IntelligentLoanApplication_Graph import HierarchicalLoanUnderwritingSystem
        
        print("Creating hierarchical loan underwriting system...")
        system = HierarchicalLoanUnderwritingSystem()
        print("✅ Hierarchical system created successfully")
        
        # Clean shutdown to prevent hanging
        print("Shutting down system...")
        system.shutdown_system()
        print("✅ System shutdown complete")
        
        return True
        
    except Exception as e:
        print(f"❌ Hierarchical system creation failed: {e}")
        # Attempt cleanup even on failure
        if system is not None:
            try:
                system.shutdown_system()
            except:
                pass  # Ignore cleanup errors
        return False

def test_basic_api_functions():
    """Test basic API functions work"""
    print("\n📊 QUICK VALIDATION: API Functions")
    print("=" * 50)
    
    try:
        from stock_price_agent import get_stock_prices
        
        print("Testing get_stock_prices with AAPL...")
        result = get_stock_prices("AAPL")
        
        if result and result.get("status") == "success":
            print("✅ Stock price API working")
            print(f"   Current AAPL price: ${result['data']['current_price']}")
            return True
        else:
            print("❌ Stock price API failed")
            return False
            
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run quick validation tests"""
    print("🚀 QUICK VALIDATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Finance Agent Creation", test_finance_agent_creation),
        ("Hierarchical System", test_hierarchical_system), 
        ("API Functions", test_basic_api_functions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            # Use timeout wrapper for potentially hanging tests
            if "Hierarchical" in test_name:
                result = run_with_timeout(test_func, timeout_seconds=45)
            else:
                result = run_with_timeout(test_func, timeout_seconds=30)
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n📊 QUICK VALIDATION RESULTS")
    print("=" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\nOverall: {passed}/{len(results)} tests passed ({success_rate:.0f}%)")
    
    if success_rate >= 66:  # At least 2/3 tests passing
        print("🎉 QUICK VALIDATION: SUCCESSFUL - Core systems operational")
        return True
    else:
        print("⚠️ QUICK VALIDATION: ISSUES DETECTED - Review failed tests")
        return False

if __name__ == "__main__":
    try:
        success = main()
        
        if not success:
            sys.exit(1)
        else:
            print("\n🎯 Quick validation completed successfully!")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)