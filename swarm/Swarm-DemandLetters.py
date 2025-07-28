#!/usr/bin/env python3
"""
Swarm-Based Legal Document Analysis for Demand Letters

This module provides a comprehensive implementation of swarm intelligence for analyzing
legal demand letters in insurance contexts. It demonstrates both collaborative and
competitive coordination patterns for thorough document review and response generation.

The module includes:
- PDF document processing for legal correspondence
- Swarm-based document analysis with collaborative and competitive patterns
- Insurance claims expertise integration
- Professional response generation
- Comparative analysis between coordination patterns
"""

import time
import logging
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import json

# Third-party imports
try:
    import PyPDF2
    from strands import Agent
    from strands_tools import swarm
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    print("Warning: Some dependencies not available. Running in demonstration mode.")
    DEPENDENCIES_AVAILABLE = False


# ==============================================================================
# LEGAL DOCUMENT PROCESSING UTILITIES
# ==============================================================================

class LegalDocumentProcessor:
    """
    Specialized processor for legal documents, particularly demand letters.
    
    This class provides functionality to extract, analyze, and prepare legal
    documents for swarm-based analysis, with specific focus on insurance
    demand letters and claims correspondence.
    """
    
    @staticmethod
    def read_legal_pdf(file_path: str) -> Dict[str, Any]:
        """
        Read and extract text from a legal PDF document with comprehensive metadata.
        
        Args:
            file_path: Path to the legal PDF document
            
        Returns:
            Dictionary containing extracted text, metadata, and analysis hints
        """
        try:
            if not DEPENDENCIES_AVAILABLE:
                return {
                    "status": "demo",
                    "message": "PyPDF2 not available - running in demo mode",
                    "text": "Demo: Legal document content would be extracted here",
                    "document_type": "legal_correspondence",
                    "pages": 0
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
                document_analysis = LegalDocumentProcessor._analyze_document_type(full_text)
                
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
                "message": f"Legal document not found: {file_path}",
                "text": "",
                "pages": 0
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing legal document: {str(e)}",
                "text": "",
                "pages": 0
            }
    
    @staticmethod
    def _analyze_document_type(text: str) -> Dict[str, Any]:
        """
        Analyze the document to identify key characteristics and type.
        
        Args:
            text: Full text content of the document
            
        Returns:
            Dictionary with document analysis results
        """
        text_lower = text.lower()
        
        # Document type indicators
        document_indicators = {
            "demand_letter": ["demand letter", "demand for payment", "demand", "notice of"],
            "legal_correspondence": ["attorney", "law firm", "legal", "counsel"],
            "insurance_claim": ["policy", "claim", "coverage", "insured", "premium"],
            "litigation_notice": ["litigation", "lawsuit", "court", "complaint"],
            "settlement": ["settlement", "resolve", "negotiate", "agreement"]
        }
        
        # Financial indicators
        financial_patterns = [
            "$", "dollars", "damages", "compensation", "payment",
            "thousand", "million", "billion"
        ]
        
        # Urgency indicators
        urgency_patterns = [
            "immediately", "urgent", "within", "days", "hours",
            "deadline", "time limit", "expedite"
        ]
        
        # Legal threat indicators
        threat_patterns = [
            "bad faith", "breach", "violation", "statutory",
            "regulatory", "compliance", "sanctions"
        ]
        
        analysis = {
            "document_type": "unknown",
            "contains_financial_demands": any(pattern in text_lower for pattern in financial_patterns),
            "contains_urgency": any(pattern in text_lower for pattern in urgency_patterns),
            "contains_legal_threats": any(pattern in text_lower for pattern in threat_patterns),
            "estimated_complexity": "medium"
        }
        
        # Determine primary document type
        for doc_type, indicators in document_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                analysis["document_type"] = doc_type
                break
        
        # Assess complexity
        complexity_score = 0
        if analysis["contains_financial_demands"]:
            complexity_score += 1
        if analysis["contains_urgency"]:
            complexity_score += 1  
        if analysis["contains_legal_threats"]:
            complexity_score += 2
        if len(text) > 5000:
            complexity_score += 1
            
        if complexity_score >= 4:
            analysis["estimated_complexity"] = "high"
        elif complexity_score <= 1:
            analysis["estimated_complexity"] = "low"
        
        return analysis


# ==============================================================================
# INSURANCE DEMAND LETTER ANALYSIS FRAMEWORK
# ==============================================================================

@dataclass
class DemandLetterAnalysis:
    """
    Structured analysis results for insurance demand letters.
    
    Attributes:
        verification: Document verification results
        classification: Urgency classification (URGENT or NORMAL)
        validation: Policy and legal validation results
        recommended_response: Generated response email
        analysis_timestamp: When analysis was performed
        coordination_pattern: Pattern used for analysis
    """
    verification: Dict[str, Any]
    classification: str
    validation: Dict[str, Any] 
    recommended_response: str
    analysis_timestamp: datetime
    coordination_pattern: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class InsuranceDemandAnalyzer:
    """
    Specialized analyzer for insurance demand letters using swarm intelligence.
    
    This class implements both collaborative and competitive swarm patterns
    to provide comprehensive analysis of legal demand letters in insurance
    contexts, generating professional responses and classifications.
    """
    
    def __init__(self):
        """Initialize the demand letter analyzer."""
        if DEPENDENCIES_AVAILABLE:
            self.swarm_agent = Agent(tools=[swarm])
            self.summarizer_agent = Agent(
                system_prompt="""You are a Senior Legal Analysis Coordinator specializing in insurance law.
                Your role is to synthesize insights from multiple legal experts and create comprehensive,
                actionable analysis for insurance demand letters. You should:
                
                • Consolidate findings from multiple expert perspectives
                • Identify critical issues requiring immediate attention
                • Provide clear classifications and recommendations
                • Generate professional, legally sound response communications
                • Highlight potential risks and opportunities
                • Ensure compliance with regulatory requirements
                
                Focus on creating clear, actionable summaries that support informed decision-making."""
            )
        else:
            self.swarm_agent = None
            self.summarizer_agent = None
            print("Running in demo mode - Strands not available")
    
    def analyze_demand_letter(self, 
                            document_text: str, 
                            coordination_pattern: str = "collaborative",
                            swarm_size: int = 3) -> DemandLetterAnalysis:
        """
        Analyze a demand letter using swarm intelligence.
        
        Args:
            document_text: Full text of the demand letter
            coordination_pattern: Either "collaborative" or "competitive"
            swarm_size: Number of agents in the swarm (1-10)
            
        Returns:
            Comprehensive analysis results
        """
        if not DEPENDENCIES_AVAILABLE:
            return self._create_demo_analysis(coordination_pattern)
        
        # Create analysis prompt
        analysis_prompt = self._create_analysis_prompt(document_text)
        
        # Run swarm analysis
        swarm_result = self.swarm_agent.tool.swarm(
            task=analysis_prompt,
            swarm_size=swarm_size,
            coordination_pattern=coordination_pattern
        )
        
        # Synthesize results using summarizer agent
        synthesis_prompt = self._create_synthesis_prompt(swarm_result)
        final_analysis = str(self.summarizer_agent(synthesis_prompt))
        
        # Parse and structure the results
        return self._parse_analysis_results(
            final_analysis, 
            coordination_pattern, 
            swarm_result
        )
    
    def _create_analysis_prompt(self, document_text: str) -> str:
        """
        Create a comprehensive analysis prompt for the swarm.
        
        Args:
            document_text: Full text of the demand letter
            
        Returns:
            Formatted analysis prompt
        """
        return f"""
        You are an Insurance Claims Legal Expert analyzing a demand letter. Your task is to review 
        the following legal correspondence and provide comprehensive analysis:

        DOCUMENT TEXT:
        {document_text}

        REQUIRED ANALYSIS:

        1) VERIFICATION: Review the letter and verify this is a legitimate demand letter from a legal firm.
           Check for proper legal formatting, signatures, case references, and formal demands.

        2) CLASSIFICATION: Carefully analyze the language and classify this document as either:
           - URGENT-RESPONSE: Amount exceeding $50,000 AND/OR response timeframe less than 3 days (72 hours)
           - NORMAL-RESPONSE: Amount less than $50,000 AND/OR more than 3 days to respond
           
           Pay special attention to monetary amounts, deadlines, and legal consequences of delay.

        3) VALIDATION: Evaluate the language and policy provisions to validate if the damages, 
           limits, and provisions are in compliance with insurance policies. Assess:
           - Coverage applicability and limits
           - Policy provision interpretations
           - Regulatory compliance issues
           - Potential bad faith exposure
           - Legitimacy of claimed damages

        4) RESPONSE EMAIL: Write a professional email response that corresponds to your classification.
           If URGENT-RESPONSE: Acknowledge urgency, take immediate action, request reasonable extension if needed
           If NORMAL-RESPONSE: Standard professional response with investigation timeline
           If groundless claims are identified: Use appropriate legal language to dispute without being dismissive

        Provide detailed reasoning for each analysis component and ensure all recommendations are 
        legally sound and professionally appropriate.
        """
    
    def _create_synthesis_prompt(self, swarm_result: Dict[str, Any]) -> str:
        """
        Create synthesis prompt for the summarizer agent.
        
        Args:
            swarm_result: Results from the swarm analysis
            
        Returns:
            Formatted synthesis prompt
        """
        return f"""
        Consolidate the analysis from the swarm and provide a comprehensive summary with the following structure:

        SWARM ANALYSIS RESULTS:
        {swarm_result.get('content', ['No content available'])[2:]}

        Please provide a clear, structured summary addressing:

        1) VERIFICATION: Is this a legitimate legal demand letter? Include evidence.

        2) CLASSIFICATION: URGENT-RESPONSE or NORMAL-RESPONSE with clear justification based on:
           - Monetary amounts demanded
           - Response timeframes required
           - Legal consequences of delayed response

        3) VALIDATION: Assessment of policy provisions, coverage issues, and legal validity including:
           - Coverage analysis and policy interpretation
           - Regulatory compliance concerns
           - Bad faith exposure assessment
           - Legitimacy of claimed damages

        4) RECOMMENDED RESPONSE EMAIL: Professional email response that:
           - Acknowledges receipt appropriately
           - Addresses urgency level correctly
           - Takes appropriate immediate actions
           - Maintains professional legal standards
           - Protects the insurance company's interests

        Ensure the analysis is comprehensive, legally sound, and actionable for insurance professionals.
        """
    
    def _parse_analysis_results(self, 
                               analysis_text: str, 
                               coordination_pattern: str,
                               swarm_result: Dict[str, Any]) -> DemandLetterAnalysis:
        """
        Parse the synthesized analysis into structured results.
        
        Args:
            analysis_text: Synthesized analysis from summarizer
            coordination_pattern: Pattern used for analysis
            swarm_result: Original swarm results
            
        Returns:
            Structured analysis results
        """
        # Simple parsing - in production, would use more sophisticated NLP
        sections = analysis_text.split("##")
        
        verification_info = {"status": "analyzed", "details": "See full analysis"}
        classification = "NORMAL-RESPONSE"  # Default
        validation_info = {"status": "reviewed", "details": "See full analysis"}
        response_email = "See full analysis for recommended response"
        
        # Extract classification if possible
        if "URGENT-RESPONSE" in analysis_text:
            classification = "URGENT-RESPONSE"
        elif "NORMAL-RESPONSE" in analysis_text:
            classification = "NORMAL-RESPONSE"
        
        # Try to extract email section
        email_markers = ["RESPONSE EMAIL", "RECOMMENDED RESPONSE", "EMAIL", "RESPONSE"]
        for marker in email_markers:
            if marker in analysis_text.upper():
                parts = analysis_text.upper().split(marker)
                if len(parts) > 1:
                    # Find the email content (simplified)
                    response_email = analysis_text  # Keep full analysis for now
                    break
        
        return DemandLetterAnalysis(
            verification=verification_info,
            classification=classification,
            validation=validation_info,
            recommended_response=response_email,
            analysis_timestamp=datetime.now(),
            coordination_pattern=coordination_pattern,
            metadata={
                "swarm_size": len(swarm_result.get('content', [])),
                "analysis_length": len(analysis_text),
                "full_swarm_result": swarm_result
            }
        )
    
    def _create_demo_analysis(self, coordination_pattern: str) -> DemandLetterAnalysis:
        """
        Create a demo analysis for when dependencies are not available.
        
        Args:
            coordination_pattern: Pattern that would have been used
            
        Returns:
            Demo analysis results
        """
        return DemandLetterAnalysis(
            verification={
                "status": "demo", 
                "details": "Would verify legal document authenticity"
            },
            classification="DEMO-ANALYSIS",
            validation={
                "status": "demo",
                "details": "Would validate policy provisions and legal claims"
            },
            recommended_response="Demo mode: Would generate professional legal response email",
            analysis_timestamp=datetime.now(),
            coordination_pattern=coordination_pattern,
            metadata={"demo_mode": True}
        )


# ==============================================================================
# COMPARATIVE ANALYSIS FRAMEWORK
# ==============================================================================

class SwarmPatternComparator:
    """
    Utility for comparing different swarm coordination patterns on the same document.
    
    This class enables side-by-side analysis using both collaborative and competitive
    patterns to understand how different coordination approaches affect analysis quality
    and recommendations.
    """
    
    def __init__(self):
        """Initialize the pattern comparator."""
        self.analyzer = InsuranceDemandAnalyzer()
    
    def compare_coordination_patterns(self, 
                                    document_text: str,
                                    swarm_size: int = 3) -> Dict[str, DemandLetterAnalysis]:
        """
        Analyze the same document using both coordination patterns for comparison.
        
        Args:
            document_text: Document text to analyze
            swarm_size: Number of agents to use in each swarm
            
        Returns:
            Dictionary with results from both patterns
        """
        print("🔄 Running comparative analysis...")
        
        # Analyze with collaborative pattern
        print("📝 Analyzing with collaborative pattern...")
        collaborative_result = self.analyzer.analyze_demand_letter(
            document_text, 
            coordination_pattern="collaborative",
            swarm_size=swarm_size
        )
        
        # Brief pause between analyses
        time.sleep(2)
        
        # Analyze with competitive pattern
        print("⚔️ Analyzing with competitive pattern...")
        competitive_result = self.analyzer.analyze_demand_letter(
            document_text,
            coordination_pattern="competitive", 
            swarm_size=swarm_size
        )
        
        return {
            "collaborative": collaborative_result,
            "competitive": competitive_result
        }
    
    def generate_comparison_report(self, 
                                 comparison_results: Dict[str, DemandLetterAnalysis]) -> str:
        """
        Generate a comparative analysis report.
        
        Args:
            comparison_results: Results from both coordination patterns
            
        Returns:
            Formatted comparison report
        """
        collaborative = comparison_results["collaborative"]
        competitive = comparison_results["competitive"]
        
        report = f"""
# SWARM COORDINATION PATTERN COMPARISON REPORT

## Analysis Overview
- Document analyzed using both collaborative and competitive swarm patterns
- Analysis timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Swarm size used: {collaborative.metadata.get('swarm_size', 'Unknown')}

## Classification Comparison

### Collaborative Pattern Result:
**Classification:** {collaborative.classification}

### Competitive Pattern Result:  
**Classification:** {competitive.classification}

**Agreement:** {'✅ MATCH' if collaborative.classification == competitive.classification else '❌ DIFFERENT'}

## Analysis Depth Comparison

### Collaborative Analysis Length:
{collaborative.metadata.get('analysis_length', 0)} characters

### Competitive Analysis Length:
{competitive.metadata.get('analysis_length', 0)} characters

## Key Differences and Insights

### Collaborative Pattern Characteristics:
- Agents build upon each other's insights
- Seeks consensus and agreement
- Tends toward comprehensive, unified analysis
- May smooth over dissenting opinions

### Competitive Pattern Characteristics:
- Agents develop independent perspectives
- Presents diverse viewpoints
- May identify more edge cases and alternative interpretations
- Can highlight areas of legitimate disagreement

## Recommendations

Based on this comparative analysis:

1. **For Complex Legal Documents**: Use competitive pattern to ensure all angles are explored
2. **For Standard Claims**: Collaborative pattern may provide more efficient, unified analysis
3. **For High-Stakes Situations**: Consider both patterns for maximum insight coverage
4. **For Time-Sensitive Analysis**: Collaborative pattern typically provides faster consensus

## Full Analysis Results

### COLLABORATIVE PATTERN ANALYSIS:
{collaborative.recommended_response}

---

### COMPETITIVE PATTERN ANALYSIS:
{competitive.recommended_response}
        """
        
        return report


# ==============================================================================
# NATURAL LANGUAGE INTERFACE FOR LEGAL ANALYSIS
# ==============================================================================

class NaturalLanguageLegalInterface:
    """
    Natural language interface for legal document analysis using swarm intelligence.
    
    This class provides conversational methods for analyzing legal documents,
    making the swarm analysis more accessible for legal professionals.
    """
    
    def __init__(self):
        """Initialize the natural language interface."""
        if DEPENDENCIES_AVAILABLE:
            self.agent = Agent(tools=[swarm])
        else:
            self.agent = None
            print("Running in demo mode - Strands not available")
    
    def analyze_legal_document_natural(self, document_text: str, request: str) -> str:
        """
        Analyze a legal document using natural language requests.
        
        Args:
            document_text: Full text of the legal document
            request: Natural language description of analysis needed
            
        Returns:
            Natural language analysis response
        """
        if not DEPENDENCIES_AVAILABLE:
            return f"Demo mode: Would analyze legal document based on request: '{request}'"
        
        full_prompt = f"""
        Please analyze this legal document using a swarm of 3 specialized agents:
        
        DOCUMENT:
        {document_text}
        
        ANALYSIS REQUEST:
        {request}
        
        Use collaborative coordination to ensure thorough analysis and provide
        practical recommendations for handling this legal correspondence.
        """
        
        response = str(self.agent(full_prompt))
        return response


# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def demonstrate_demand_letter_analysis():
    """
    Demonstrate comprehensive demand letter analysis using both coordination patterns.
    
    Returns:
        Dictionary with demonstration results
    """
    print("📋 LEGAL DEMAND LETTER ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Load sample legal document
    print("📄 Loading sample legal correspondence...")
    doc_processor = LegalDocumentProcessor()
    sample_doc = doc_processor.read_legal_pdf("data/LEGALCORRESPONDENCE.pdf")
    
    if sample_doc["status"] != "success":
        print(f"⚠️ Could not load sample document: {sample_doc['message']}")
        # Use sample text for demo
        sample_text = """
        LEGAL CORRESPONDENCE: PRIVILEGED & CONFIDENTIAL
        
        DEMAND LETTER AND NOTICE OF BAD FAITH CLAIMS HANDLING PRACTICES
        
        This firm represents Westlake Commercial Properties, LLC regarding insurance claim 
        PIN-2022-78549 for damages exceeding $1,000,000 from December 8, 2022 flood event.
        
        We demand immediate payment of $1,000,000.00 within 72 hours or we will pursue
        bad faith litigation under Washington Insurance Fair Conduct Act.
        
        Failure to respond within this timeframe will be deemed a waiver of all policy limits.
        """
    else:
        sample_text = sample_doc["text"][:2000]  # Use first 2000 chars for demo
        print(f"✅ Loaded document: {sample_doc['pages']} pages, {sample_doc['total_chars']} characters")
    
    # Run comparative analysis
    print("\n🔍 Running comparative swarm analysis...")
    comparator = SwarmPatternComparator()
    
    comparison_results = comparator.compare_coordination_patterns(
        document_text=sample_text,
        swarm_size=3
    )
    
    # Generate comparison report
    print("\n📊 Generating comparison report...")
    comparison_report = comparator.generate_comparison_report(comparison_results)
    
    print("✅ Analysis complete!")
    
    return {
        "document_info": sample_doc,
        "comparison_results": comparison_results,
        "comparison_report": comparison_report
    }


def demonstrate_natural_language_interface():
    """
    Demonstrate the natural language interface for legal analysis.
    
    Returns:
        Dictionary with demonstration results
    """
    print("💬 NATURAL LANGUAGE LEGAL ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    nl_interface = NaturalLanguageLegalInterface()
    
    # Sample legal text
    sample_legal_text = """
    DEMAND FOR PAYMENT
    
    Dear Insurance Company,
    
    Our client sustained $75,000 in water damage to their commercial property.
    Your adjuster improperly denied coverage citing a wear and tear exclusion.
    
    We demand payment of the full $75,000 within 10 days or we will file suit
    for breach of contract and bad faith.
    
    Sincerely,
    Legal Counsel
    """
    
    # Different analysis requests
    analysis_requests = [
        "Determine if this is urgent and requires immediate attention",
        "Assess the legal validity of the coverage denial claims",
        "Draft a professional response that protects our interests"
    ]
    
    results = {}
    
    for i, request in enumerate(analysis_requests, 1):
        print(f"\n📝 Analysis Request {i}: {request}")
        
        result = nl_interface.analyze_legal_document_natural(
            sample_legal_text, 
            request
        )
        
        results[f"request_{i}"] = {
            "request": request,
            "analysis": result
        }
        
        print(f"✅ Analysis {i} complete")
    
    return results


def explain_swarm_patterns_for_legal_analysis():
    """
    Explain how different swarm patterns apply to legal document analysis.
    
    Returns:
        Dictionary with pattern explanations
    """
    return {
        "collaborative_pattern": {
            "description": "Agents work together building consensus on legal interpretation",
            "benefits": [
                "Unified, coherent analysis and recommendations",
                "Reduces conflicting interpretations",  
                "Faster consensus on standard legal issues",
                "Good for routine claims and correspondence"
            ],
            "use_cases": [
                "Standard insurance claims review",
                "Routine contract interpretation",
                "Policy compliance assessments",
                "Non-controversial legal correspondence"
            ]
        },
        
        "competitive_pattern": {
            "description": "Agents develop independent perspectives on legal issues",
            "benefits": [
                "Identifies diverse legal interpretations and risks",
                "Uncovers edge cases and alternative arguments",
                "Provides multiple strategic options",
                "Highlights areas of legitimate legal debate"
            ],
            "use_cases": [
                "Complex litigation preparation",
                "High-stakes demand letter analysis",
                "Ambiguous policy interpretation",
                "Bad faith claims assessment"
            ]
        },
        
        "selection_guidance": {
            "high_stakes": "Use competitive pattern for maximum insight coverage",
            "routine_matters": "Use collaborative pattern for efficient consensus",
            "time_sensitive": "Collaborative typically faster for urgent responses",
            "complex_legal": "Competitive pattern explores more interpretations",
            "best_practice": "Use both patterns for critical legal decisions"
        }
    }


# ==============================================================================
# MAIN EXECUTION AND INTERACTIVE EXAMPLES
# ==============================================================================

def main():
    """
    Main function providing comprehensive legal document analysis demonstrations.
    
    This function serves as the entry point for exploring swarm-based legal
    analysis when the module is executed directly.
    """
    print(__doc__)
    print("\n🚀 Starting Legal Document Swarm Analysis...")
    
    # Explain swarm patterns for legal context
    print("\n📚 SWARM PATTERNS FOR LEGAL ANALYSIS")
    pattern_explanations = explain_swarm_patterns_for_legal_analysis()
    
    for pattern, info in pattern_explanations.items():
        if pattern != "selection_guidance":
            print(f"\n{pattern.upper().replace('_', ' ')}:")
            print(f"Description: {info['description']}")
            print(f"Benefits: {', '.join(info['benefits'][:2])}...")
    
    # Run demonstrations
    print("\n" + "=" * 60)
    print("🎬 RUNNING LEGAL ANALYSIS DEMONSTRATIONS")
    
    demo_results = {}
    
    # Demand letter analysis demonstration
    demo_results["demand_analysis"] = demonstrate_demand_letter_analysis()
    
    # Natural language interface demonstration
    demo_results["natural_language"] = demonstrate_natural_language_interface()
    
    # Show selection guidance
    print("\n📋 PATTERN SELECTION GUIDANCE")
    guidance = pattern_explanations["selection_guidance"]
    for situation, recommendation in guidance.items():
        print(f"• {situation.replace('_', ' ').title()}: {recommendation}")
    
    # Provide usage guidance
    print("\n" + "=" * 60)
    print("🛠️ AVAILABLE CLASSES AND FUNCTIONS:")
    print("• LegalDocumentProcessor: PDF processing for legal documents")
    print("• InsuranceDemandAnalyzer: Specialized demand letter analysis")
    print("• SwarmPatternComparator: Compare collaborative vs competitive patterns")
    print("• NaturalLanguageLegalInterface: Conversational legal analysis")
    
    print("\n💡 Getting Started Tips:")
    print("• Use InsuranceDemandAnalyzer for comprehensive demand letter review")
    print("• Try SwarmPatternComparator to see how patterns differ")
    print("• Use competitive pattern for high-stakes legal analysis")
    print("• Use collaborative pattern for routine legal correspondence")
    print("• Natural language interface makes analysis more accessible")
    
    return demo_results


if __name__ == "__main__":
    main()