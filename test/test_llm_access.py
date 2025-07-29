#!/usr/bin/env python3
"""
Test actual LLM model access via Strands Agents.

This test specifically tries to invoke AWS Bedrock LLM models to verify
we have proper model access permissions, not just connectivity.
"""

import sys
import os
from dotenv import load_dotenv

# Add the Finance-assistant-swarm-agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Finance-assistant-swarm-agent'))

def test_agent_llm_invocation():
    """Test that we can actually invoke the LLM via a Strands Agent"""
    print("🤖 TESTING ACTUAL LLM MODEL ACCESS")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    try:
        from stock_price_agent import create_stock_price_agent
        
        print("Creating stock price agent...")
        agent = create_stock_price_agent()
        print("✅ Agent created successfully")
        
        # Try a simple query that should invoke the LLM
        test_query = "What is the current price of AAPL stock?"
        print(f"Testing LLM invocation with query: '{test_query}'")
        
        # This should trigger the LLM model
        response = agent(test_query)
        
        print("✅ LLM invocation successful!")
        print(f"Response preview: {str(response)[:200]}...")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ LLM invocation failed: {error_msg}")
        
        # Check for specific access denied errors
        if "AccessDeniedException" in error_msg:
            print("🚨 SPECIFIC ISSUE: AWS Bedrock model access denied")
            print("   - You need to request model access in AWS Console")
            print("   - Go to: AWS Console → Bedrock → Model Access")
            print("   - Request access to: amazon.nova-pro-v1:0")
        elif "region" in error_msg.lower():
            print("🚨 SPECIFIC ISSUE: Region-related error")
            print(f"   - Current AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION')}")
        elif "credentials" in error_msg.lower():
            print("🚨 SPECIFIC ISSUE: AWS credentials problem")
        
        return False

def test_direct_bedrock_model():
    """Test BedrockModel directly to isolate the issue"""
    print("\n🔧 TESTING DIRECT BEDROCKMODEL ACCESS")
    print("=" * 50)
    
    load_dotenv()
    
    try:
        from strands.models.bedrock import BedrockModel
        
        region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')
        model_id = "us.amazon.nova-pro-v1:0"
        
        print(f"Creating BedrockModel (ID: {model_id}, Region: {region})...")
        model = BedrockModel(model_id=model_id, region=region)
        
        print("✅ BedrockModel created")
        
        # Try a simple completion
        print("Testing model completion...")
        response = model.complete("Hello, this is a test. Please respond with 'Test successful'.")
        
        print("✅ Model completion successful!")
        print(f"Response: {response}")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Direct model access failed: {error_msg}")
        
        if "AccessDeniedException" in error_msg:
            print("🚨 CONFIRMED: AWS Bedrock model access permission denied")
            print("   This is the root cause of the test failures.")
        
        return False

def main():
    """Run LLM access tests"""
    print("🧪 LLM MODEL ACCESS TEST SUITE")
    print("=" * 60)
    
    # Test 1: Agent-based LLM invocation
    agent_success = test_agent_llm_invocation()
    
    # Test 2: Direct BedrockModel access  
    model_success = test_direct_bedrock_model()
    
    # Summary
    print(f"\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    print(f"Agent LLM Access: {'✅ PASS' if agent_success else '❌ FAIL'}")
    print(f"Direct Model Access: {'✅ PASS' if model_success else '❌ FAIL'}")
    
    if agent_success and model_success:
        print(f"\n🎉 ALL TESTS PASSED! LLM model access is working.")
    else:
        print(f"\n⚠️  LLM ACCESS ISSUES DETECTED")
        print("   Root cause: AWS Bedrock model access permissions")
        print("   Solution: Request model access in AWS Console")
    
    return agent_success and model_success

if __name__ == "__main__":
    success = main()
    
    if not success:
        sys.exit(1)