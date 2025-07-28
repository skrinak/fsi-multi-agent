#!/usr/bin/env python3
"""
Test script to verify dotenv loading works correctly.
"""

import os
from dotenv import load_dotenv

print("Testing dotenv loading...")

# Try current directory
load_dotenv()
print(f"After load_dotenv(): FINNHUB_API_KEY = {os.getenv('FINNHUB_API_KEY', 'NOT_FOUND')}")

# Try parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
print(f"After load_dotenv('.env'): FINNHUB_API_KEY = {os.getenv('FINNHUB_API_KEY', 'NOT_FOUND')}")

# Check if .env file exists
env_path = '.env'
if os.path.exists(env_path):
    print(f"✅ Found .env file at: {os.path.abspath(env_path)}")
else:
    print(f"❌ No .env file found at: {os.path.abspath(env_path)}")
    print("ℹ️ You need to create a .env file based on env.example")
    print("Example: cp env.example .env")

# Show all environment variables starting with FINNHUB
finnhub_vars = {k: v for k, v in os.environ.items() if k.startswith('FINNHUB')}
if finnhub_vars:
    print(f"Found FINNHUB environment variables: {list(finnhub_vars.keys())}")
else:
    print("No FINNHUB environment variables found")