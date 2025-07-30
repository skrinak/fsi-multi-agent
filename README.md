# Multi-Agent Systems for Financial Services
## A Self-Study Guide to Agentic AI Architecture Development

## 🚨 BUILT WITH STRANDS AGENTS SDK (TOP PRIORITY)

**This repository prioritizes Strands Agents SDK above all other frameworks**. Every implementation, example, and educational content demonstrates Strands SDK best practices as the primary multi-agent development framework.

*This work is a derivative of original research and principles developed for the broader financial services technical community. We acknowledge and credit the original author's foundational work, Alfredo Castillo, Sr Solutions Architect – FSI GenAI at AWS, in multi-agent system design principles.*

---

## Table of Contents

- [Introduction to Agentic AI and Multi-Agent Systems](documentation/INTRODUCTION_TO_AGENTIC_AI.md)
- [Multi-Agent Coordination Patterns](documentation/COORDINATION_PATTERNS.md)
- [Core Design Principles](documentation/DESIGN_PRINCIPLES.md)
- [Implementation Examples](documentation/IMPLEMENTATION_EXAMPLES.md)
- [Learning Path: A Progressive Journey Through Multi-Agent Systems](documentation/LEARNING_PATH.md)
- [Additional Learning Resources](documentation/LEARNING_RESOURCES.md)
- [Setup Requirements & Installation](#setup-requirements--installation)
- [Quick Start Guide](#quick-start-guide)

---

## Setup Requirements & Installation

### Prerequisites

- **Python 3.10+** with pip package manager
- **AWS Account** with programmatic access credentials  
- **uv Package Manager** (recommended) - Install with: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Git** for repository cloning
- **Internet Connection** for API access (AWS Bedrock, Financial Modeling Prep, Finnhub for real-time quotes)
- **Minimum 4GB RAM** for concurrent multi-agent execution
- **Basic Knowledge**: Understanding of large language models and command-line tools

### System Compatibility

- **macOS**: Full support (tested on macOS 14+)
- **Linux**: Full support (tested on Ubuntu 20.04+)  
- **Windows**: Full support with PowerShell or WSL2

### Required Environment Variables

Create a `.env` file in the project root with the following **essential variables**:

```bash
# AWS Configuration (REQUIRED)
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_DEFAULT_REGION=your_preferred_aws_region  # e.g., us-west-2, us-east-1, eu-west-1

# Financial Data APIs (REQUIRED)
FINNHUB_API_KEY=your_finnhub_api_key_here  # For real-time quotes only
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here  # For historical data

# Optional: Enhanced Financial Data (Free Tiers Available)
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
FINANCIAL_MODELING_PREP_API_KEY=your_fmp_key_here
NEWS_API_KEY=your_news_api_key_here
```

**How to obtain API keys:**

1. **AWS Credentials**: 
   - Create AWS account at [aws.amazon.com](https://aws.amazon.com)
   - Create IAM user with programmatic access
   - Attach `AmazonBedrockFullAccess` policy
   - Save Access Key ID and Secret Access Key

2. **Financial Data APIs**: 
   - **Financial Modeling Prep**: Sign up at [financialmodelingprep.com](https://financialmodelingprep.com) for historical data
   - **Finnhub API**: Sign up at [finnhub.io/dashboard](https://finnhub.io/dashboard) for real-time quotes (60 calls/minute on free tier)

### AWS Bedrock Model Access (CRITICAL)

The system requires access to **exactly 3 foundation models** in your configured AWS region. **Global Flexibility**: This system works in any AWS region where these Bedrock models are available - simply set your preferred region in `AWS_DEFAULT_REGION`.

| Model Name | Model ID | Usage | Required For |
|------------|----------|-------|---------------|
| **Amazon Nova Pro** | `amazon.nova-pro-v1:0` | Primary LLM for finance agents | Finance Assistant, Stock Analysis |
| **Claude 3.5 Sonnet** | `anthropic.claude-3-5-sonnet-20241022-v2:0` | Complex reasoning tasks | Loan Underwriting, Claims |
| **Claude 3.5 Haiku** | `anthropic.claude-3-5-haiku-20241022-v1:0` | Fast operations | Quick validations, Summaries |

**To request model access:**

1. Navigate to [AWS Console → Bedrock → Model Access](https://console.aws.amazon.com/bedrock/home#/modelaccess)
2. **Select your preferred AWS region** where Bedrock is available (the system will use your `AWS_DEFAULT_REGION` setting)
3. Request access to the 3 models listed above
4. Wait for approval (typically 2-24 hours)
5. Verify access: `python -c "import boto3, os; from dotenv import load_dotenv; load_dotenv(); region=os.getenv('AWS_DEFAULT_REGION', 'us-west-2'); print(f'Models available in {region}: {len(boto3.client(\"bedrock\", region_name=region).list_foundation_models()[\"modelSummaries\"])}')"`

### Installation Steps

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd fsi-multi-agent
   ```

2. **Install uv Package Manager** (if not installed)
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Create Environment File**
   ```bash
   cp env.example .env
   # Edit .env with your actual API keys (replace placeholder values)
   ```

4. **Install Dependencies**
   ```bash
   # Finance agents (primary system)
   cd Finance-assistant-swarm-agent
   uv sync
   cd ..
   
   # Multi-agent pattern dependencies
   cd swarm && pip install -r requirements.txt && cd ..
   cd graph_IntelligentLoanUnderwriting && pip install -r requirements.txt && cd ..
   cd WorkFlow_ClaimsAdjudication && pip install -r requirements.txt && cd ..
   ```

5. **Verify Installation**
   ```bash
   python test/test_aws_region.py
   python test/test_quick_validation.py  # Should show 3/3 tests passing
   ```

   **Expected Output**: All validation tests should pass (3/3) confirming:
   - ✅ Finance Agent Creation
   - ✅ Hierarchical System 
   - ✅ API Functions (Multi-Agent Systems data integration)

## Quick Start Guide

### Running the 5 Multi-Agent Demos

All demos can be executed using uv for optimal dependency management:

#### 1. Finance Assistant Swarm (Collaborative Pattern)
```bash
cd Finance-assistant-swarm-agent
uv run finance_assistant_swarm.py
```
**What it does**: Collaborative swarm of 4 specialized finance agents providing comprehensive stock analysis through shared memory coordination.

#### 2. Hierarchical Loan Underwriting (Authority Delegation Pattern)
```bash
uv run --with-requirements graph_IntelligentLoanUnderwriting/requirements.txt \
    python graph_IntelligentLoanUnderwriting/IntelligentLoanApplication_Graph.py
```
**What it does**: 3-tier hierarchical system with executive-manager-specialist roles processing loan applications through PDF document analysis and fraud detection.

#### 3. Mesh Swarm Financial Research (Peer-to-Peer Pattern)  
```bash
uv run --with-requirements swarm/requirements.txt \
    python swarm/FinancialResearch_MeshSwarm.py
```
**What it does**: Mesh communication pattern where research agents collaborate directly, sharing insights for multi-perspective financial analysis.

#### 4. Sequential Claims Adjudication (Workflow Pattern)
```bash
uv run --with-requirements WorkFlow_ClaimsAdjudication/requirements.txt \
    python WorkFlow_ClaimsAdjudication/ClaimsAdjudication_SequentialPattern.py
```
**What it does**: 6-stage sequential workflow processing First Notification of Loss (FNOL) through fraud detection, policy verification, and settlement calculation.

#### 5. Loop Pattern Financial Analysis (Iterative Refinement)
```bash
cd Finance-assistant-swarm-agent
uv run stock_price_agent.py
# Demonstrates iterative refinement through multiple analysis rounds
```
**What it does**: Iterative refinement cycles where agents progressively improve analysis quality through feedback loops and convergence detection.

### Troubleshooting Common Issues

**AWS Access Denied Error:**
```bash
# Verify region consistency
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(f'Region: {os.getenv(\"AWS_DEFAULT_REGION\")}')"

# Test Bedrock connectivity  
python -c "import boto3, os; from dotenv import load_dotenv; load_dotenv(); print(f'Models available: {len(boto3.client(\"bedrock\", region_name=os.getenv(\"AWS_DEFAULT_REGION\")).list_foundation_models()[\"modelSummaries\"])}')"

# Verify specific model access
python -c "import boto3, os; from dotenv import load_dotenv; load_dotenv(); models = boto3.client('bedrock', region_name=os.getenv('AWS_DEFAULT_REGION')).list_foundation_models()['modelSummaries']; nova = [m for m in models if 'nova-pro' in m['modelId']]; print(f'Nova Pro available: {len(nova) > 0}')"
```

**Missing Dependencies:**
```bash
# Reinstall all requirements
find . -name "requirements.txt" -exec pip install -r {} \;

# Verify core dependencies
python -c "import strands; print('Strands SDK: OK')"
python -c "import boto3; print('AWS SDK: OK')"
python -c "import finnhub; print('Finnhub SDK: OK')"
```

**Demo Execution Issues:**
```bash
# Test each pattern individually
python test/test_quick_validation.py

# Verify uv installation and configuration
uv --version
cd Finance-assistant-swarm-agent && uv check
```

**API Rate Limits:**
- **Financial Modeling Prep**: 250 calls/day (free tier) - primary data source for historical data
- **Finnhub**: 60 calls/minute (free tier) - real-time quotes only, implement delays if needed
- **AWS Bedrock**: Model-specific limits - use exponential backoff
- **Alpha Vantage**: 500 requests/day (free tier)

**Performance Optimization:**
- Run demos sequentially to avoid resource contention
- Monitor system memory usage during multi-agent execution  
- Use `uv run --isolated` for clean environments
- Set `PYTHONPATH` if imports fail: `export PYTHONPATH=$PWD:$PYTHONPATH`

---

*This educational resource is designed to provide a comprehensive introduction to multi-agent AI systems through practical, real-world financial services applications. The combination of theoretical foundations and hands-on implementation provides learners with both conceptual understanding and practical skills needed for modern AI system development.*