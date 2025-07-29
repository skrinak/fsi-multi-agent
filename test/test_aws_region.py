#!/usr/bin/env python3
"""
Simple test to verify AWS_DEFAULT_REGION environment variable usage.

This test verifies that:
1. AWS_DEFAULT_REGION is properly loaded from .env file
2. AWS Bedrock connectivity works with the configured region
3. BedrockModel can be instantiated using the environment variable
"""

import sys
import os
from dotenv import load_dotenv

# Add the Finance-assistant-swarm-agent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Finance-assistant-swarm-agent'))

def test_aws_region_loading():
    """Test that AWS_DEFAULT_REGION is properly loaded from .env"""
    print("🔧 TESTING AWS_DEFAULT_REGION ENVIRONMENT VARIABLE")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check if AWS_DEFAULT_REGION is set
    aws_region = os.getenv('AWS_DEFAULT_REGION')
    
    if aws_region:
        print(f"✅ AWS_DEFAULT_REGION loaded: {aws_region}")
        return True, aws_region
    else:
        print("❌ AWS_DEFAULT_REGION not found in environment")
        return False, None

def test_bedrock_connectivity(region):
    """Test AWS Bedrock connectivity using the region from environment"""
    print(f"\n🔗 TESTING AWS BEDROCK CONNECTIVITY (Region: {region})")
    print("-" * 50)
    
    try:
        import boto3
        
        # Create Bedrock client with the configured region
        client = boto3.client('bedrock', region_name=region)
        
        # Test connectivity by listing available models
        print("Attempting to list foundation models...")
        models_response = client.list_foundation_models()
        model_count = len(models_response.get('modelSummaries', []))
        
        print(f"✅ Successfully connected to AWS Bedrock")
        print(f"✅ Found {model_count} available models in {region}")
        
        # Check for Nova Pro model specifically
        nova_models = [m for m in models_response.get('modelSummaries', []) 
                      if 'nova-pro' in m.get('modelId', '').lower()]
        
        if nova_models:
            print(f"✅ Nova Pro models available: {len(nova_models)}")
            for model in nova_models[:3]:  # Show first 3
                print(f"   - {model['modelId']}")
        else:
            print("⚠️  Nova Pro models not found")
        
        return True
        
    except Exception as e:
        print(f"❌ AWS Bedrock connectivity failed: {e}")
        return False

def test_bedrock_model_creation(region):
    """Test BedrockModel creation using the environment variable"""
    print(f"\n🤖 TESTING BEDROCKMODEL CREATION (Region: {region})")
    print("-" * 50)
    
    try:
        from strands.models.bedrock import BedrockModel
        
        # Create BedrockModel using environment variable region
        print("Creating BedrockModel with environment region...")
        model = BedrockModel(
            model_id="us.amazon.nova-pro-v1:0", 
            region=region
        )
        
        print(f"✅ BedrockModel created successfully")
        print(f"✅ Model ID: us.amazon.nova-pro-v1:0")
        print(f"✅ Region: {region}")
        
        return True
        
    except Exception as e:
        print(f"❌ BedrockModel creation failed: {e}")
        return False

def main():
    """Run all AWS region tests"""
    print("🧪 AWS REGION CONFIGURATION TEST SUITE")
    print("=" * 60)
    
    # Test 1: Environment variable loading
    region_loaded, region = test_aws_region_loading()
    if not region_loaded:
        print("\n❌ CRITICAL: Cannot proceed without AWS_DEFAULT_REGION")
        return False
    
    # Test 2: Bedrock connectivity
    bedrock_connected = test_bedrock_connectivity(region)
    
    # Test 3: BedrockModel creation
    model_created = test_bedrock_model_creation(region)
    
    # Summary
    print(f"\n📊 TEST RESULTS SUMMARY")
    print("=" * 30)
    print(f"Environment Loading: {'✅ PASS' if region_loaded else '❌ FAIL'}")
    print(f"Bedrock Connectivity: {'✅ PASS' if bedrock_connected else '❌ FAIL'}")
    print(f"BedrockModel Creation: {'✅ PASS' if model_created else '❌ FAIL'}")
    
    all_passed = region_loaded and bedrock_connected and model_created
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED! AWS region configuration is working correctly.")
        print(f"✅ Region '{region}' is properly configured and accessible.")
    else:
        print(f"\n⚠️  SOME TESTS FAILED. Check AWS configuration and model access.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    
    if not success:
        sys.exit(1)