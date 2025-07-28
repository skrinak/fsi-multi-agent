#!/usr/bin/env python3
"""
Automated Financial Research & Analysis using Swarm of Agents with Strands Agents

This module provides a comprehensive implementation of multi-agent systems using mesh swarm architecture
for financial analysis. It demonstrates how specialized agents can work together to analyze complex
financial documents and provide investment recommendations through collective intelligence.

The module includes:
- PDF document processing for financial reports
- Mesh swarm architecture with specialized financial agents
- Collaborative analysis using shared memory and agent communication
- Investment recommendation generation based on multi-perspective analysis
- Educational examples of swarm intelligence patterns
"""

import time
import json
import logging
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime

# Third-party imports
try:
    import PyPDF2
    import boto3
    import yaml
    from strands import Agent
    from strands_tools import swarm
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    print("Warning: Some dependencies not available. Running in demonstration mode.")
    DEPENDENCIES_AVAILABLE = False


# ==============================================================================
# MULTI-AGENT SYSTEMS AND SWARM INTELLIGENCE CONCEPTS
# ==============================================================================

class SwarmIntelligenceConcepts:
    """
    Educational class explaining swarm intelligence and multi-agent system fundamentals.
    
    This class provides comprehensive documentation of the theoretical foundations
    for building effective multi-agent financial analysis systems.
    """
    
    @staticmethod
    def explain_swarm_intelligence() -> Dict[str, str]:
        """
        Explains the core concepts of swarm intelligence and multi-agent systems.
        
        Returns:
            Dictionary mapping concept names to detailed explanations
        """
        return {
            "swarm_intelligence": """
                SWARM INTELLIGENCE:
                An agent swarm is a collection of autonomous AI agents working together to solve 
                complex problems through collaboration. Inspired by natural systems like ant colonies 
                or bird flocks, agent swarms leverage collective intelligence where the combined output 
                exceeds what any single agent could produce.
                
                Key Characteristics:
                • Distributed Problem Solving: Breaking complex tasks into subtasks for parallel processing
                • Information Sharing: Agents exchange insights to build collective knowledge
                • Specialization: Different agents focus on specific aspects of a problem
                • Redundancy: Multiple agents working on similar tasks improve reliability
                • Emergent Intelligence: The system exhibits capabilities beyond individual components
            """,
            
            "multi_agent_systems": """
                MULTI-AGENT SYSTEMS:
                Multi-agent systems consist of multiple interacting intelligent agents within an 
                environment. These systems enable sophisticated problem-solving through:
                
                • Decentralized Control: No single agent directs the entire system
                • Local Interactions: Agents primarily interact with nearby agents
                • Simple Rules: Individual agents follow relatively simple behaviors
                • Emergent Complexity: Complex system behavior emerges from simple agent interactions
                • Collective Intelligence: The group achieves better results than individuals
            """,
            
            "mesh_architecture": """
                MESH ARCHITECTURE:
                In a mesh architecture, all agents can communicate directly with each other,
                enabling rich information exchange and collaborative problem-solving:
                
                • Direct Communication: Every agent can communicate with every other agent
                • Rich Information Flow: Multiple pathways for information sharing
                • Parallel Processing: Agents can work simultaneously on different aspects
                • Collaborative Refinement: Agents build upon each other's insights
                • Fault Tolerance: Multiple communication paths provide redundancy
            """
        }
    
    @staticmethod
    def financial_analysis_applications() -> Dict[str, Any]:
        """
        Explains how swarm intelligence applies to financial analysis.
        
        Returns:
            Dictionary with financial analysis applications and benefits
        """
        return {
            "applications": [
                "Investment opportunity evaluation",
                "Risk assessment and mitigation",
                "Market research and analysis",
                "Financial report interpretation",
                "Portfolio optimization",
                "Regulatory compliance analysis"
            ],
            
            "agent_specializations": {
                "research_agent": "Gathers and analyzes factual information and data",
                "investment_agent": "Evaluates creative investment approaches and opportunities",
                "risk_agent": "Identifies potential risks and analyzes investment proposals",
                "summarizer_agent": "Synthesizes insights into comprehensive recommendations"
            },
            
            "benefits": [
                "Multiple expert perspectives on complex financial decisions",
                "Reduced bias through diverse analytical approaches",
                "Comprehensive risk assessment from specialized agents",
                "Enhanced accuracy through collaborative validation",
                "Scalable analysis for large volumes of financial data"
            ]
        }


# ==============================================================================
# PDF DOCUMENT PROCESSING FOR FINANCIAL REPORTS
# ==============================================================================

class FinancialReportProcessor:
    """
    Specialized processor for financial documents, particularly 10-K reports and financial statements.
    
    This class provides functionality to extract and prepare financial documents
    for analysis by agent swarms, with specific focus on SEC filings and 
    corporate financial reports.
    """
    
    @staticmethod
    def read_financial_pdf(file_path: str) -> Dict[str, Any]:
        """
        Read and extract text from a financial PDF document with comprehensive error handling.
        
        Args:
            file_path: Path to the financial PDF document
            
        Returns:
            Dictionary containing extracted text, metadata, and document information
        """
        try:
            if not DEPENDENCIES_AVAILABLE:
                return {
                    "status": "demo",
                    "message": "PyPDF2 not available - running in demo mode",
                    "text": "Demo: Financial report content would be extracted here",
                    "pages": 0,
                    "document_type": "financial_report"
                }
            
            # Open and read the PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from all pages
                full_text = ""
                page_contents = []
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    full_text += page_text + "\n\n"
                    
                    page_contents.append({
                        "page_number": page_num + 1,
                        "text": page_text,
                        "char_count": len(page_text)
                    })
                
                # Analyze document characteristics
                document_analysis = FinancialReportProcessor._analyze_financial_document(full_text)
                
                return {
                    "status": "success",
                    "text": full_text,
                    "pages": num_pages,
                    "page_details": page_contents,
                    "total_chars": len(full_text),
                    "file_path": file_path,
                    "document_analysis": document_analysis
                }
        
        except FileNotFoundError:
            return {
                "status": "error",
                "message": f"Financial document not found: {file_path}",
                "text": "",
                "pages": 0
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing financial document: {str(e)}",
                "text": "",
                "pages": 0
            }
    
    @staticmethod
    def _analyze_financial_document(text: str) -> Dict[str, Any]:
        """
        Analyze the document to identify key financial document characteristics.
        
        Args:
            text: Full text content of the document
            
        Returns:
            Dictionary with document analysis results
        """
        text_lower = text.lower()
        
        # Document type indicators
        document_indicators = {
            "10k_report": ["form 10-k", "annual report", "sec filing"],
            "10q_report": ["form 10-q", "quarterly report"],
            "earnings_report": ["earnings", "quarterly results", "financial results"],
            "analyst_report": ["analyst", "research report", "investment recommendation"],
            "prospectus": ["prospectus", "offering", "securities"]
        }
        
        # Financial metrics indicators
        financial_indicators = [
            "revenue", "earnings", "ebitda", "net income", "cash flow",
            "balance sheet", "assets", "liabilities", "equity"
        ]
        
        # Risk indicators
        risk_indicators = [
            "risk factors", "forward-looking", "uncertainty", "competition",
            "regulatory", "market risk", "credit risk"
        ]
        
        analysis = {
            "document_type": "unknown",
            "contains_financial_metrics": any(indicator in text_lower for indicator in financial_indicators),
            "contains_risk_factors": any(indicator in text_lower for indicator in risk_indicators),
            "estimated_complexity": "medium"
        }
        
        # Determine primary document type
        for doc_type, indicators in document_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                analysis["document_type"] = doc_type
                break
        
        # Assess complexity
        complexity_score = 0
        if analysis["contains_financial_metrics"]:
            complexity_score += 1
        if analysis["contains_risk_factors"]:
            complexity_score += 1
        if len(text) > 50000:
            complexity_score += 2
        if "form 10-k" in text_lower:
            complexity_score += 1
            
        if complexity_score >= 4:
            analysis["estimated_complexity"] = "high"
        elif complexity_score <= 1:
            analysis["estimated_complexity"] = "low"
        
        return analysis


# ==============================================================================
# MESH SWARM FINANCIAL ANALYSIS FRAMEWORK
# ==============================================================================

@dataclass
class FinancialAnalysisResult:
    """
    Structured results from financial analysis swarm.
    
    Attributes:
        research_insights: Findings from research agent
        investment_evaluation: Assessment from investment agent
        risk_analysis: Risk evaluation results
        final_recommendation: Synthesized recommendation
        analysis_timestamp: When analysis was performed
        confidence_score: Overall confidence in the analysis
    """
    research_insights: str
    investment_evaluation: str
    risk_analysis: str
    final_recommendation: str
    analysis_timestamp: datetime
    confidence_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class MeshSwarmFinancialAnalyzer:
    """
    Mesh swarm implementation for comprehensive financial analysis.
    
    This class creates a network of specialized financial agents that work together
    to analyze financial documents and provide investment recommendations through
    collaborative intelligence and multi-perspective analysis.
    """
    
    def __init__(self):
        """Initialize the mesh swarm financial analyzer."""
        if DEPENDENCIES_AVAILABLE:
            self._create_specialized_agents()
            self.swarm_agent = Agent(tools=[swarm])
        else:
            print("Running in demo mode - Strands not available")
            self.agents = None
            self.swarm_agent = None
    
    def _create_specialized_agents(self):
        """Create the specialized financial analysis agents."""
        self.agents = {
            "research": Agent(
                system_prompt="""You are a Financial Research Agent specializing in gathering and analyzing information.
                Your role in the swarm is to provide factual information and research insights on financial topics.
                You should focus on providing accurate data and identifying key aspects of financial problems.
                When receiving input from other agents, evaluate if their information aligns with your research.
                
                Your analysis should cover:
                • Financial statement analysis and key metrics
                • Industry context and competitive positioning
                • Historical performance trends
                • Regulatory and compliance considerations
                • Market conditions and economic factors
                """,
                callback_handler=None
            ),
            
            "investment": Agent(
                system_prompt="""You are an Investment Agent specializing in evaluating innovative approaches to new investments.
                Your role in the swarm is to think strategically about investment opportunities and propose creative approaches.
                You should build upon information from other agents while adding your unique investment perspective.
                Focus on approaches that create long-term value and competitive advantages.
                
                Your analysis should cover:
                • Investment thesis and value proposition
                • Growth potential and market opportunities
                • Strategic positioning and competitive advantages
                • Capital allocation and financial strategy
                • Long-term value creation potential
                """,
                callback_handler=None
            ),
            
            "risk": Agent(
                system_prompt="""You are a Risk Analysis Agent specializing in analyzing investment proposals and identifying risks.
                Your role in the swarm is to evaluate investments proposed by other agents and identify potential issues.
                You should carefully examine proposed investments, find weaknesses or oversights, and suggest improvements.
                Be constructive in your analysis while ensuring the final solution addresses all significant risks.
                
                Your analysis should cover:
                • Financial risks and credit considerations
                • Market and competitive risks
                • Operational and management risks
                • Regulatory and compliance risks
                • Scenario analysis and stress testing
                """,
                callback_handler=None
            ),
            
            "summarizer": Agent(
                system_prompt="""You are a Summarizer Agent specializing in synthesizing financial information.
                Your role in the swarm is to gather insights from all agents and create a cohesive final investment recommendation.
                You should combine the best ideas and address the risks to create a comprehensive response.
                Focus on creating a clear, actionable summary that addresses the original query effectively.
                
                Your synthesis should include:
                • Executive summary with clear recommendation
                • Key strengths and investment highlights
                • Significant risks and mitigation strategies
                • Financial projections and valuation considerations
                • Implementation recommendations and next steps
                """
            )
        }
    
    def analyze_financial_document(self, 
                                 document_text: str, 
                                 query: str = None,
                                 use_mesh_communication: bool = True) -> FinancialAnalysisResult:
        """
        Analyze a financial document using the mesh swarm.
        
        Args:
            document_text: Full text of the financial document
            query: Specific analysis question (optional)
            use_mesh_communication: Whether to use mesh communication pattern
            
        Returns:
            Comprehensive financial analysis results
        """
        if not DEPENDENCIES_AVAILABLE:
            return self._create_demo_analysis()
        
        if not query:
            query = f"""
            Analyze this financial report and provide an investment recommendation:
            
            {document_text[:5000]}...
            
            Please provide a comprehensive analysis including financial performance,
            growth prospects, risks, and whether this represents a good investment opportunity.
            """
        
        if use_mesh_communication:
            return self._mesh_analysis(query, document_text)
        else:
            # Use built-in swarm tool for comparison
            return self._swarm_tool_analysis(query)
    
    def _mesh_analysis(self, query: str, document_text: str) -> FinancialAnalysisResult:
        """
        Perform analysis using mesh communication pattern.
        
        Args:
            query: Analysis query
            document_text: Financial document content
            
        Returns:
            Structured analysis results
        """
        # Dictionary to track messages between agents (mesh communication)
        messages = {
            "research": [],
            "investment": [],
            "risk": [],
            "summarizer": []
        }
        
        print("🔍 Phase 1: Initial analysis by each specialized agent...")
        
        # Phase 1: Initial analysis by each specialized agent
        research_result = str(self.agents["research"](query))
        time.sleep(2)  # Rate limiting
        
        investment_result = str(self.agents["investment"](query))
        time.sleep(2)
        
        risk_result = str(self.agents["risk"](query))
        time.sleep(2)
        
        print("🔄 Sharing results with all agents (mesh communication)...")
        
        # Share results with all other agents (mesh communication)
        messages["investment"].append(f"From Research Agent: {research_result}")
        messages["risk"].append(f"From Research Agent: {research_result}")
        messages["summarizer"].append(f"From Research Agent: {research_result}")
        
        messages["research"].append(f"From Investment Agent: {investment_result}")
        messages["risk"].append(f"From Investment Agent: {investment_result}")
        messages["summarizer"].append(f"From Investment Agent: {investment_result}")
        
        messages["research"].append(f"From Risk Agent: {risk_result}")
        messages["investment"].append(f"From Risk Agent: {risk_result}")
        messages["summarizer"].append(f"From Risk Agent: {risk_result}")
        
        print("🔧 Phase 2: Each agent refines based on input from others...")
        
        # Phase 2: Each agent refines based on input from others
        research_prompt = f"{query}\n\nConsider these messages from other agents:\n" + "\n\n".join(messages["research"])
        investment_prompt = f"{query}\n\nConsider these messages from other agents:\n" + "\n\n".join(messages["investment"])
        risk_prompt = f"{query}\n\nConsider these messages from other agents:\n" + "\n\n".join(messages["risk"])
        
        refined_research = str(self.agents["research"](research_prompt))
        time.sleep(2)
        
        refined_investment = str(self.agents["investment"](investment_prompt))
        time.sleep(2)
        
        refined_risk = str(self.agents["risk"](risk_prompt))
        time.sleep(2)
        
        # Share refined results with summarizer
        messages["summarizer"].append(f"From Research Agent (Phase 2): {refined_research}")
        messages["summarizer"].append(f"From Investment Agent (Phase 2): {refined_investment}")
        messages["summarizer"].append(f"From Risk Agent (Phase 2): {refined_risk}")
        
        print("📊 Final phase: Synthesizing comprehensive solution...")
        
        # Final phase: Summarizer creates the final solution
        summarizer_prompt = f"""
        Original query: {query}
        
        Please synthesize the following inputs from all agents into a comprehensive final solution:
        
        {chr(10).join(messages["summarizer"])}
        
        Create a well-structured final answer that incorporates the research findings, 
        investment ideas, and addresses the risk feedback.
        Provide a clear recommendation on whether to invest in this company or not.
        Provide rationale to support your recommendation with specific financial metrics and analysis.
        """
        
        final_solution = str(self.agents["summarizer"](summarizer_prompt))
        
        return FinancialAnalysisResult(
            research_insights=refined_research,
            investment_evaluation=refined_investment,
            risk_analysis=refined_risk,
            final_recommendation=final_solution,
            analysis_timestamp=datetime.now(),
            confidence_score=0.85,  # Could be calculated based on agent agreement
            metadata={
                "communication_pattern": "mesh",
                "agents_used": 4,
                "phases_completed": 2
            }
        )
    
    def _swarm_tool_analysis(self, query: str) -> FinancialAnalysisResult:
        """
        Perform analysis using the built-in swarm tool for comparison.
        
        Args:
            query: Analysis query
            
        Returns:
            Structured analysis results
        """
        print("🔧 Using built-in swarm tool for analysis...")
        
        swarm_result = self.swarm_agent.tool.swarm(
            task=query,
            swarm_size=4,
            coordination_pattern="collaborative"
        )
        
        return FinancialAnalysisResult(
            research_insights="Generated using swarm tool",
            investment_evaluation="Generated using swarm tool",
            risk_analysis="Generated using swarm tool",
            final_recommendation=str(swarm_result),
            analysis_timestamp=datetime.now(),
            confidence_score=0.80,
            metadata={
                "communication_pattern": "swarm_tool",
                "agents_used": 4,
                "coordination": "collaborative"
            }
        )
    
    def _create_demo_analysis(self) -> FinancialAnalysisResult:
        """
        Create a demo analysis for when dependencies are not available.
        
        Returns:
            Demo analysis results
        """
        return FinancialAnalysisResult(
            research_insights="Demo: Would provide comprehensive financial research insights",
            investment_evaluation="Demo: Would evaluate investment opportunities and strategies",
            risk_analysis="Demo: Would identify and analyze potential investment risks",
            final_recommendation="Demo: Would provide final investment recommendation with rationale",
            analysis_timestamp=datetime.now(),
            confidence_score=0.0,
            metadata={"demo_mode": True}
        )


# ==============================================================================
# SHARED MEMORY IMPLEMENTATION FOR ENHANCED SWARM COORDINATION
# ==============================================================================

class SharedMemorySystem:
    """
    Shared memory system for enhanced swarm coordination and knowledge persistence.
    
    This system provides centralized knowledge storage and retrieval for agent swarms,
    enabling more sophisticated coordination and historical knowledge preservation.
    """
    
    def __init__(self):
        """Initialize the shared memory system."""
        self.memory_store = {
            "financial_insights": [],
            "investment_analyses": [],
            "risk_assessments": [],
            "market_context": [],
            "historical_decisions": []
        }
        self.access_lock = {}  # Simplified thread safety placeholder
    
    def store_insight(self, category: str, agent_id: str, insight: str, metadata: Dict[str, Any] = None):
        """
        Store an insight in shared memory.
        
        Args:
            category: Category of insight
            agent_id: ID of the agent providing the insight
            insight: The insight content
            metadata: Additional metadata about the insight
        """
        if category not in self.memory_store:
            self.memory_store[category] = []
        
        insight_entry = {
            "agent_id": agent_id,
            "content": insight,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.memory_store[category].append(insight_entry)
    
    def retrieve_insights(self, category: str = None, agent_id: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve insights from shared memory.
        
        Args:
            category: Specific category to retrieve (optional)
            agent_id: Specific agent ID to filter by (optional)
            
        Returns:
            List of matching insights
        """
        if category and category in self.memory_store:
            insights = self.memory_store[category]
        else:
            # Return all insights from all categories
            insights = []
            for cat_insights in self.memory_store.values():
                insights.extend(cat_insights)
        
        # Filter by agent_id if specified
        if agent_id:
            insights = [insight for insight in insights if insight["agent_id"] == agent_id]
        
        return insights
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the current memory state.
        
        Returns:
            Dictionary with memory statistics and summary
        """
        summary = {
            "total_insights": sum(len(insights) for insights in self.memory_store.values()),
            "categories": {
                category: len(insights) 
                for category, insights in self.memory_store.items()
            },
            "last_updated": datetime.now().isoformat()
        }
        
        return summary


# ==============================================================================
# COMPARATIVE ANALYSIS AND BENCHMARKING
# ==============================================================================

class SwarmPatternComparator:
    """
    Utility for comparing different swarm coordination patterns on financial analysis tasks.
    
    This class enables side-by-side comparison of mesh communication versus
    built-in swarm tools to understand performance and output quality differences.
    """
    
    def __init__(self):
        """Initialize the pattern comparator."""
        self.analyzer = MeshSwarmFinancialAnalyzer()
    
    def compare_analysis_patterns(self, 
                                document_text: str, 
                                query: str = None) -> Dict[str, FinancialAnalysisResult]:
        """
        Compare mesh communication versus swarm tool analysis on the same document.
        
        Args:
            document_text: Financial document text to analyze
            query: Analysis query (optional)
            
        Returns:
            Dictionary with results from both patterns
        """
        print("🔄 Running comparative analysis...")
        
        # Analyze with mesh communication pattern
        print("📝 Analyzing with mesh communication pattern...")
        mesh_result = self.analyzer.analyze_financial_document(
            document_text, 
            query, 
            use_mesh_communication=True
        )
        
        # Brief pause between analyses
        time.sleep(5)
        
        # Analyze with swarm tool
        print("⚙️ Analyzing with built-in swarm tool...")
        swarm_result = self.analyzer.analyze_financial_document(
            document_text,
            query,
            use_mesh_communication=False
        )
        
        return {
            "mesh_communication": mesh_result,
            "swarm_tool": swarm_result
        }
    
    def generate_comparison_report(self, 
                                 comparison_results: Dict[str, FinancialAnalysisResult]) -> str:
        """
        Generate a comparative analysis report.
        
        Args:
            comparison_results: Results from both coordination patterns
            
        Returns:
            Formatted comparison report
        """
        mesh_result = comparison_results["mesh_communication"]
        swarm_result = comparison_results["swarm_tool"]
        
        report = f"""
# SWARM COORDINATION PATTERN COMPARISON REPORT

## Analysis Overview
- Financial document analyzed using both mesh communication and swarm tool patterns
- Analysis timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Agents used: {mesh_result.metadata.get('agents_used', 'Unknown')}

## Pattern Comparison

### Mesh Communication Pattern:
**Confidence Score:** {mesh_result.confidence_score}
**Phases Completed:** {mesh_result.metadata.get('phases_completed', 'Unknown')}
**Communication Type:** Direct agent-to-agent mesh communication

### Swarm Tool Pattern:
**Confidence Score:** {swarm_result.confidence_score}
**Coordination:** {swarm_result.metadata.get('coordination', 'Unknown')}
**Communication Type:** Built-in swarm coordination

## Key Differences and Insights

### Mesh Communication Characteristics:
- Agents communicate directly with each other in multiple phases
- Rich information exchange between all agents
- Iterative refinement based on peer feedback
- More complex coordination but potentially richer insights

### Swarm Tool Characteristics:
- Streamlined coordination through built-in mechanisms
- Efficient processing with less manual coordination
- Consistent results through standardized patterns
- Faster execution with built-in optimizations

## Recommendations

Based on this comparative analysis:

1. **For Complex Financial Analysis**: Mesh communication provides richer multi-perspective insights
2. **For Rapid Analysis**: Swarm tool offers faster, streamlined processing
3. **For Iterative Refinement**: Mesh pattern enables more thorough collaborative refinement
4. **For Production Systems**: Swarm tool provides more consistent and reliable results

## Full Analysis Results

### MESH COMMUNICATION ANALYSIS:
{mesh_result.final_recommendation}

---

### SWARM TOOL ANALYSIS:
{swarm_result.final_recommendation}
        """
        
        return report


# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def demonstrate_financial_mesh_swarm():
    """
    Demonstrate comprehensive financial analysis using mesh swarm architecture.
    
    Returns:
        Dictionary with demonstration results
    """
    print("📊 FINANCIAL MESH SWARM DEMONSTRATION")
    print("=" * 60)
    
    # Sample financial document path
    sample_document_path = "data/amzn-20241231-10K-Part-1&2.pdf"
    
    # Load and process financial document
    print("📄 Loading financial document...")
    processor = FinancialReportProcessor()
    doc_data = processor.read_financial_pdf(sample_document_path)
    
    if doc_data["status"] != "success":
        print(f"⚠️ Could not load document: {doc_data['message']}")
        # Use sample financial text for demo
        sample_text = """
        AMAZON.COM, INC. ANNUAL REPORT (Form 10-K)
        
        We seek to be Earth's most customer-centric company. We are guided by four principles: 
        customer obsession rather than competitor focus, passion for invention, commitment to 
        operational excellence, and long-term thinking.
        
        Revenue increased 11% to $637.96 billion in 2024, compared with $574.79 billion in 2023.
        North America segment revenue increased 10% year-over-year to $387.50 billion.
        International segment revenue increased 9% year-over-year to $142.91 billion.
        AWS segment revenue increased 19% year-over-year to $107.56 billion.
        
        Operating cash flow increased to $115.88 billion in 2024, compared with $84.95 billion in 2023.
        """
        doc_data["text"] = sample_text
    else:
        print(f"✅ Loaded document: {doc_data['pages']} pages, {doc_data['total_chars']} characters")
    
    # Create mesh swarm analyzer
    print("\n🔍 Creating mesh swarm financial analyzer...")
    analyzer = MeshSwarmFinancialAnalyzer()
    
    # Perform financial analysis
    analysis_query = """
    Analyze this financial report and determine if this is a good company to invest in.
    Consider financial performance, growth prospects, competitive position, and risks.
    Provide a clear investment recommendation with supporting rationale.
    """
    
    print("\n📈 Conducting comprehensive financial analysis...")
    analysis_result = analyzer.analyze_financial_document(
        doc_data["text"], 
        analysis_query
    )
    
    print("✅ Financial analysis complete!")
    
    return {
        "document_info": doc_data,
        "analysis_result": analysis_result,
        "timestamp": datetime.now().isoformat()
    }


def demonstrate_pattern_comparison():
    """
    Demonstrate comparative analysis between different swarm patterns.
    
    Returns:
        Dictionary with comparison results
    """
    print("🔄 SWARM PATTERN COMPARISON DEMONSTRATION")
    print("=" * 60)
    
    # Sample financial text for comparison
    sample_financial_text = """
    TECHNOLOGY COMPANY QUARTERLY RESULTS
    
    Revenue: $12.5B (+15% YoY)
    Net Income: $2.8B (+22% YoY)
    Cash Flow: $3.1B (+18% YoY)
    
    Strong performance in cloud services and AI products.
    Expanding into new markets with strategic acquisitions.
    Facing increased competition and regulatory scrutiny.
    """
    
    print("📊 Running comparative analysis...")
    comparator = SwarmPatternComparator()
    
    comparison_results = comparator.compare_analysis_patterns(
        sample_financial_text,
        "Analyze this company's financial performance and provide investment recommendation"
    )
    
    # Generate comparison report
    print("\n📋 Generating comparison report...")
    comparison_report = comparator.generate_comparison_report(comparison_results)
    
    print("✅ Pattern comparison complete!")
    
    return {
        "comparison_results": comparison_results,
        "comparison_report": comparison_report
    }


def demonstrate_shared_memory_system():
    """
    Demonstrate shared memory system for enhanced swarm coordination.
    
    Returns:
        Dictionary with shared memory demonstration results
    """
    print("💭 SHARED MEMORY SYSTEM DEMONSTRATION")
    print("=" * 60)
    
    # Create shared memory system
    shared_memory = SharedMemorySystem()
    
    # Simulate agents storing insights
    print("📝 Simulating agents storing insights...")
    
    shared_memory.store_insight(
        "financial_insights", 
        "research_agent", 
        "Company shows strong revenue growth of 15% YoY",
        {"confidence": 0.9, "source": "10-K filing"}
    )
    
    shared_memory.store_insight(
        "investment_analyses",
        "investment_agent",
        "Strong competitive position in cloud computing market",
        {"confidence": 0.85, "market_segment": "cloud"}
    )
    
    shared_memory.store_insight(
        "risk_assessments",
        "risk_agent", 
        "Regulatory scrutiny poses potential risk to operations",
        {"risk_level": "medium", "probability": 0.6}
    )
    
    # Retrieve and display insights
    print("\n🔍 Retrieving stored insights...")
    all_insights = shared_memory.retrieve_insights()
    
    print(f"Total insights stored: {len(all_insights)}")
    for insight in all_insights:
        print(f"- {insight['agent_id']}: {insight['content']}")
    
    # Display memory summary
    print("\n📊 Memory system summary:")
    summary = shared_memory.get_memory_summary()
    print(f"Total insights: {summary['total_insights']}")
    print(f"Categories: {summary['categories']}")
    
    return {
        "shared_memory": shared_memory,
        "insights_stored": len(all_insights),
        "memory_summary": summary
    }


def explain_swarm_applications():
    """
    Explain when and how to use swarm intelligence for financial analysis.
    
    Returns:
        Dictionary with application guidance
    """
    return {
        "when_to_use_swarm": [
            "For quick, parallel processing of complex financial documents",
            "When you need multiple expert perspectives on investment decisions",
            "For tasks that benefit from collective intelligence and debate",
            "When analyzing large volumes of financial data requiring specialization",
            "For comprehensive risk assessment from multiple angles"
        ],
        
        "swarm_vs_single_agent": {
            "advantages": [
                "Multiple specialized perspectives reduce bias",
                "Collective intelligence improves accuracy",
                "Parallel processing increases efficiency",
                "Cross-validation improves reliability",
                "Enhanced risk identification through diverse viewpoints"
            ],
            "considerations": [
                "Higher computational costs with multiple agents",
                "More complex coordination and communication",
                "Potential for conflicting recommendations requiring resolution",
                "Longer processing time for thorough multi-agent analysis"
            ]
        },
        
        "best_practices": [
            "Define clear roles and specializations for each agent",
            "Implement effective communication patterns (mesh, hierarchical, etc.)",
            "Use shared memory for knowledge persistence and coordination",
            "Build in validation and consensus mechanisms",
            "Monitor and optimize agent interactions for efficiency",
            "Test with smaller problems before scaling to complex analyses"
        ],
        
        "implementation_patterns": {
            "mesh_communication": "Best for collaborative analysis requiring rich information exchange",
            "swarm_tool": "Best for streamlined processing and consistent results",
            "shared_memory": "Best for knowledge persistence and complex coordination",
            "hybrid_approach": "Combine patterns based on specific analysis requirements"
        }
    }


# ==============================================================================
# MAIN EXECUTION AND INTERACTIVE EXAMPLES
# ==============================================================================

def main():
    """
    Main function providing comprehensive financial swarm analysis demonstrations.
    
    This function serves as the entry point for exploring swarm-based financial
    analysis when the module is executed directly.
    """
    print(__doc__)
    print("\n🚀 Starting Financial Swarm Analysis Exploration...")
    
    # Explain core concepts
    print("\n📚 SWARM INTELLIGENCE CONCEPTS")
    concepts = SwarmIntelligenceConcepts()
    core_concepts = concepts.explain_swarm_intelligence()
    
    for concept, explanation in core_concepts.items():
        print(f"\n{concept.upper().replace('_', ' ')}:")
        print(explanation)
    
    # Show financial applications
    print("\n💰 FINANCIAL ANALYSIS APPLICATIONS")
    applications = concepts.financial_analysis_applications()
    
    print("Key Applications:")
    for app in applications["applications"]:
        print(f"• {app}")
    
    print("\nAgent Specializations:")
    for role, description in applications["agent_specializations"].items():
        print(f"• {role}: {description}")
    
    # Run demonstrations
    print("\n" + "=" * 60)
    print("🎬 RUNNING FINANCIAL SWARM DEMONSTRATIONS")
    
    demo_results = {}
    
    # Financial mesh swarm demonstration
    demo_results["mesh_swarm"] = demonstrate_financial_mesh_swarm()
    
    # Pattern comparison demonstration
    demo_results["pattern_comparison"] = demonstrate_pattern_comparison()
    
    # Shared memory system demonstration
    demo_results["shared_memory"] = demonstrate_shared_memory_system()
    
    # Show application guidance
    print("\n📋 SWARM APPLICATION GUIDANCE")
    guidance = explain_swarm_applications()
    
    print("When to Use Swarm Intelligence:")
    for use_case in guidance["when_to_use_swarm"]:
        print(f"• {use_case}")
    
    print("\nBest Practices:")
    for practice in guidance["best_practices"]:
        print(f"• {practice}")
    
    # Provide usage guidance
    print("\n" + "=" * 60)
    print("🛠️ AVAILABLE CLASSES AND FUNCTIONS:")
    print("• SwarmIntelligenceConcepts: Core concepts and theory")
    print("• FinancialReportProcessor: PDF processing for financial documents")
    print("• MeshSwarmFinancialAnalyzer: Mesh swarm analysis implementation")
    print("• SwarmPatternComparator: Compare different coordination patterns")
    print("• SharedMemorySystem: Enhanced coordination and knowledge persistence")
    
    print("\n💡 Getting Started Tips:")
    print("• Use MeshSwarmFinancialAnalyzer for comprehensive financial analysis")
    print("• Try SwarmPatternComparator to see how different patterns perform")
    print("• Use mesh communication for complex, multi-perspective analysis")
    print("• Use swarm tool for efficient, streamlined processing")
    print("• Implement SharedMemorySystem for enhanced coordination")
    print("• Start with smaller documents before analyzing large financial reports")
    
    return demo_results


if __name__ == "__main__":
    main()