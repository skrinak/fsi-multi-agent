#!/usr/bin/env python3
"""
Intelligent Loan Application Processing using Multi-Agent Systems with Strands Agents

This module provides a comprehensive implementation of an intelligent loan underwriting system
using hierarchical multi-agent architecture. It demonstrates how specialized agents can work
together in a structured hierarchy to process loan applications through systematic evaluation
across multiple domains.

The module includes:
- PDF document processing for loan application materials
- Hierarchical agent graph architecture for loan underwriting
- Specialized agents for financial analysis, risk assessment, and fraud detection
- Comprehensive loan evaluation and decision-making processes
- Educational examples of multi-agent collaboration patterns
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
    from botocore.config import Config
    from strands import Agent
    from strands_tools import agent_graph
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    print("Warning: Some dependencies not available. Running in demonstration mode.")
    DEPENDENCIES_AVAILABLE = False


# ==============================================================================
# MULTI-AGENT SYSTEMS AND LOAN UNDERWRITING CONCEPTS
# ==============================================================================

class LoanUnderwritingConcepts:
    """
    Educational class explaining loan underwriting processes and multi-agent system principles.
    
    This class provides comprehensive documentation of the theoretical foundations
    for building effective multi-agent loan processing systems.
    """
    
    @staticmethod
    def explain_underwriting_process() -> Dict[str, str]:
        """
        Explains the comprehensive loan underwriting process and its components.
        
        Returns:
            Dictionary mapping process components to detailed explanations
        """
        return {
            "loan_underwriting_overview": """
                LOAN UNDERWRITING PROCESS:
                The loan underwriting process involves systematic evaluation of loan applications 
                through multiple specialized tasks across different domains:
                
                1. Financial Analysis
                   • Application Intake & Validation
                   • Credit Assessment
                   • Income & Employment Verification
                   • Asset Verification
                   • Property Appraisal (if applicable)
                
                2. Risk Analysis
                   • Risk Assessment & Scoring
                   • Fraud Detection & Prevention
                   • Market & Economic Risk Factors
                
                3. Compliance & Regulatory Review
                   • Policy Adherence Verification
                   • Regulatory Compliance Checks
                   • Documentation Standards
                
                4. Final Decision & Documentation
                   • Comprehensive Decision Analysis
                   • Policy Generation & Documentation
                   • Audit Trail Creation
            """,
            
            "multi_agent_principles": """
                MULTI-AGENT SYSTEM PRINCIPLES FOR LOAN UNDERWRITING:
                
                Principle #1: Use Case Qualification
                • Do not force-fit workloads into collaboration patterns
                • Identify business decision frictions and design workflows around proper patterns
                
                Principle #2: Enterprise Productivity Design
                • Use agentic systems when decision automation is needed
                • Focus on enterprise-scale productivity, not just individual task augmentation
                
                Principle #3: Acknowledge Trade-offs
                • Balance agency, control, and reliability in system design
                • Consider the implications of autonomous decision-making
                
                Principle #4: Share Context
                • Provide full context and complete history of agent interactions
                • Avoid isolating individual messages from broader context
                
                Principle #5: Recognize Action-Decision Relationships
                • Every action reflects an underlying decision
                • Avoid semantic ambiguity and conflicting actions
                • Ensure consistency in multi-agent decision-making
            """,
            
            "hierarchical_topology": """
                HIERARCHICAL TOPOLOGY FOR LOAN UNDERWRITING:
                Tree structure with parent-child relationships, ideal for layered processing 
                and clear reporting lines in financial services:
                
                • Loan Underwriting Supervisor: Executive-level coordination and final decisions
                • Financial Analysis Manager: Coordinates credit and verification specialists
                • Risk Analysis Manager: Oversees risk calculation and fraud detection
                • Specialist Agents: Domain experts in credit, verification, risk, and fraud
                • Documentation Agent: Handles policy creation and audit compliance
                
                Benefits:
                • Clear authority and responsibility lines
                • Scalable organizational structure
                • Efficient task delegation and escalation
                • Natural workflow progression through expertise layers
            """
        }
    
    @staticmethod
    def agent_specializations() -> Dict[str, Dict[str, Any]]:
        """
        Provides detailed specifications for each agent in the loan underwriting system.
        
        Returns:
            Dictionary with agent roles and their specialized functions
        """
        return {
            "supervisor_agent": {
                "role": "Executive Orchestration",
                "responsibilities": [
                    "Receive and validate loan applications",
                    "Coordinate with manager agents for task execution",
                    "Monitor progress and handle escalations",
                    "Aggregate results from all assessment domains",
                    "Make final loan approval/rejection decisions",
                    "Ensure compliance with lending policies and regulations",
                    "Generate final underwriting reports"
                ],
                "decision_criteria": [
                    "Credit score thresholds",
                    "Debt-to-income ratios",
                    "Collateral value assessment",
                    "Risk assessment scores",
                    "Regulatory compliance status"
                ]
            },
            
            "financial_analysis_manager": {
                "role": "Financial Coordination",
                "responsibilities": [
                    "Coordinate tasks between credit assessment and verification agents",
                    "Share required data between financial specialists",
                    "Provide overall financial analysis and creditworthiness assessment",
                    "Synthesize financial insights for supervisor decision-making"
                ]
            },
            
            "risk_analysis_manager": {
                "role": "Risk Coordination", 
                "responsibilities": [
                    "Coordinate risk scoring and probability analysis",
                    "Oversee fraud detection processes",
                    "Analyze market and economic risk factors",
                    "Evaluate borrower risk profile",
                    "Assess collateral and security risks",
                    "Provide consolidated risk assessment"
                ],
                "risk_categories": [
                    "Credit risk (default probability)",
                    "Fraud risk (application authenticity)",
                    "Market risk (economic factors)",
                    "Operational risk (process failures)",
                    "Concentration risk (portfolio impact)"
                ]
            },
            
            "specialist_agents": {
                "credit_assessment": "Comprehensive credit evaluation and scoring",
                "verification": "Income, employment, and asset validation",
                "risk_calculation": "Quantitative risk modeling and analysis",
                "fraud_detection": "Fraudulent application identification",
                "documentation": "Policy creation and audit compliance"
            }
        }


# ==============================================================================
# PDF DOCUMENT PROCESSING FOR LOAN APPLICATIONS
# ==============================================================================

class LoanDocumentProcessor:
    """
    Specialized processor for loan application documents and financial paperwork.
    
    This class provides functionality to extract and prepare loan-related documents
    for analysis by agent networks, with specific focus on credit reports, bank
    statements, tax documents, and loan applications.
    """
    
    @staticmethod
    def read_loan_pdf(file_path: str) -> Dict[str, Any]:
        """
        Read and extract text from a loan-related PDF document with comprehensive error handling.
        
        Args:
            file_path: Path to the loan document PDF
            
        Returns:
            Dictionary containing extracted text, metadata, and document information
        """
        try:
            if not DEPENDENCIES_AVAILABLE:
                return {
                    "status": "demo",
                    "message": "PyPDF2 not available - running in demo mode",
                    "text": "Demo: Loan document content would be extracted here",
                    "pages": 0,
                    "document_type": "loan_document"
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
                document_analysis = LoanDocumentProcessor._analyze_loan_document(full_text, file_path)
                
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
                "message": f"Loan document not found: {file_path}",
                "text": "",
                "pages": 0
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing loan document: {str(e)}",
                "text": "",
                "pages": 0
            }
    
    @staticmethod
    def _analyze_loan_document(text: str, file_path: str) -> Dict[str, Any]:
        """
        Analyze the document to identify loan document type and key characteristics.
        
        Args:
            text: Full text content of the document
            file_path: Path to the document for additional context
            
        Returns:
            Dictionary with document analysis results
        """
        text_lower = text.lower()
        filename_lower = file_path.lower()
        
        # Document type indicators
        document_indicators = {
            "credit_report": ["credit report", "fico", "credit score", "payment history"],
            "bank_statement": ["bank statement", "account balance", "transaction history", "deposits"],
            "pay_stub": ["pay stub", "payroll", "gross pay", "net pay", "year to date"],
            "tax_return": ["tax return", "form 1040", "adjusted gross income", "irs"],
            "loan_application": ["loan application", "mortgage application", "borrower information"],
            "property_info": ["property", "appraisal", "market value", "square feet"],
            "id_verification": ["identification", "driver license", "passport", "social security"]
        }
        
        # Financial indicators
        financial_indicators = [
            "income", "salary", "wages", "assets", "liabilities", "debt",
            "credit", "score", "balance", "payment"
        ]
        
        # Risk indicators
        risk_indicators = [
            "late payment", "delinquent", "default", "bankruptcy", "foreclosure",
            "judgment", "collection", "charge off"
        ]
        
        analysis = {
            "document_type": "unknown",
            "contains_financial_data": any(indicator in text_lower for indicator in financial_indicators),
            "contains_risk_factors": any(indicator in text_lower for indicator in risk_indicators),
            "estimated_importance": "medium"
        }
        
        # Determine document type from filename first
        for doc_type, indicators in document_indicators.items():
            if any(indicator.replace(" ", "").replace("_", "") in filename_lower.replace(" ", "").replace("_", "") for indicator in [doc_type]):
                analysis["document_type"] = doc_type
                break
        
        # If not found in filename, check content
        if analysis["document_type"] == "unknown":
            for doc_type, indicators in document_indicators.items():
                if any(indicator in text_lower for indicator in indicators):
                    analysis["document_type"] = doc_type
                    break
        
        # Assess importance
        importance_score = 0
        if analysis["contains_financial_data"]:
            importance_score += 2
        if analysis["contains_risk_factors"]:
            importance_score += 2
        if analysis["document_type"] in ["credit_report", "loan_application", "bank_statement"]:
            importance_score += 1
        if len(text) > 5000:
            importance_score += 1
            
        if importance_score >= 4:
            analysis["estimated_importance"] = "high"
        elif importance_score <= 1:
            analysis["estimated_importance"] = "low"
        
        return analysis


# ==============================================================================
# HIERARCHICAL LOAN UNDERWRITING SYSTEM
# ==============================================================================

@dataclass
class LoanApplicationPackage:
    """
    Container for all loan application documents and extracted data.
    
    Attributes:
        applicant_name: Name of the loan applicant
        documents: Dictionary of document types to extracted content
        application_id: Unique identifier for the application
        received_date: When the application was received
        document_analysis: Analysis results for each document
    """
    applicant_name: str
    documents: Dict[str, str]
    application_id: str
    received_date: datetime
    document_analysis: Dict[str, Any] = field(default_factory=dict)
    processing_status: str = "received"


@dataclass
class LoanDecision:
    """
    Comprehensive loan decision with supporting analysis.
    
    Attributes:
        decision: Final decision (APPROVED, DENIED, PENDING)
        confidence_score: Confidence in the decision (0-1)
        financial_analysis: Results from financial analysis
        risk_assessment: Risk analysis results
        fraud_indicators: Fraud detection results
        compliance_status: Regulatory compliance check results
        recommendations: Additional recommendations or conditions
        decision_timestamp: When the decision was made
    """
    decision: str
    confidence_score: float
    financial_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    fraud_indicators: List[str]
    compliance_status: str
    recommendations: List[str]
    decision_timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class HierarchicalLoanUnderwritingSystem:
    """
    Comprehensive loan underwriting system using hierarchical multi-agent architecture.
    
    This class creates and manages a network of specialized agents organized in a
    hierarchical structure to process loan applications through systematic evaluation
    across financial analysis, risk assessment, and fraud detection domains.
    """
    
    def __init__(self, graph_id: str = "loan_underwriting_system"):
        """Initialize the hierarchical loan underwriting system."""
        self.graph_id = graph_id
        self.document_processor = LoanDocumentProcessor()
        
        if DEPENDENCIES_AVAILABLE:
            self.agent = Agent(tools=[agent_graph])
            self._create_loan_underwriting_hierarchy()
        else:
            print("Running in demo mode - Strands not available")
            self.agent = None
    
    def _create_loan_underwriting_hierarchy(self):
        """Create the hierarchical agent network for loan underwriting."""
        try:
            result = self.agent.tool.agent_graph(
                action="create",
                graph_id=self.graph_id,
                topology={
                    "type": "hierarchical",
                    "nodes": [
                        {
                            "id": "loan_underwriting_supervisor_agent",
                            "role": "executive", 
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Loan Underwriting Supervisor Agent responsible for orchestrating the complete loan underwriting process. Your responsibilities include:

                            1. Receive and validate loan applications
                            2. Coordinate with manager agents to execute underwriting tasks
                            3. Monitor progress and handle escalations
                            4. Aggregate results from all assessment domains
                            5. Make final loan approval/rejection decisions based on comprehensive analysis
                            6. Ensure compliance with lending policies and regulations
                            7. Generate final underwriting reports

                            Process Flow:
                            - Start with financial analysis and application validation
                            - Then continue with risk and fraud analysis
                            - Delegate tasks to appropriate manager agents
                            - Monitor and coordinate parallel processing
                            - Collect and analyze results from all domains
                            - Apply business rules and lending policies
                            - Make final decision and generate documentation
                            - Share required information needed by each task

                            Decision Criteria:
                            - Credit score thresholds
                            - Debt-to-income ratios
                            - Collateral value
                            - Risk assessment scores
                            - Regulatory compliance status

                            Provide comprehensive analysis with clear recommendations and supporting rationale.
                            """
                        },
                        {
                            "id": "financial_analysis_manager",
                            "role": "manager",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0", 
                            "system_prompt": """
                            You are the Financial Analysis Manager responsible for comprehensive credit evaluation and income verification.
                            Your tasks include:

                            1. Coordinate tasks between the Credit Assessment Agent and the Verification Agent
                            2. Share required data between the Credit Assessment Agent and the Verification Agent
                            3. Provide overall financial analysis and creditworthiness assessment
                            4. Synthesize financial insights for supervisor decision-making

                            Focus on thorough financial evaluation and clear communication of findings.
                            """
                        },
                        {
                            "id": "risk_analysis_manager",
                            "role": "manager",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Risk Analysis Manager responsible for evaluating loan risks and detecting potential fraud. Your duties include:

                            1. Coordinate risk scoring and probability analysis
                            2. Oversee fraud detection processes
                            3. Analyze market and economic risk factors
                            4. Evaluate borrower risk profile
                            5. Assess collateral and security risks
                            6. Provide consolidated risk assessment

                            Risk Categories:
                            - Credit risk (default probability)
                            - Fraud risk (application authenticity)
                            - Market risk (economic factors)
                            - Operational risk (process failures)
                            - Concentration risk (portfolio impact)

                            Provide quantitative risk assessments with clear explanations.
                            """
                        },
                        {
                            "id": "credit_assessment_agent",
                            "role": "specialist",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Credit Assessment Agent responsible for comprehensive credit evaluation. Your tasks include:

                            1. Analyze credit history patterns and trends
                            2. Evaluate credit utilization and payment history
                            3. Assess credit mix and account age
                            4. Identify credit red flags or concerns
                            5. Provide consolidated credit assessment summary

                            Focus Areas:
                            - FICO/VantageScore analysis
                            - Credit report anomalies
                            - Recent credit inquiries
                            - Derogatory marks evaluation
                            - Credit stability assessment

                            Provide quantitative scores and qualitative insights for decision-making.
                            """
                        },
                        {
                            "id": "verification_agent",
                            "role": "specialist",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Verification Agent responsible for validating applicant financial information. Your responsibilities include:

                            1. Validate income verification through multiple sources
                            2. Verify employment status and stability
                            3. Verify asset declarations and documentation
                            4. Cross-reference financial statements
                            5. Identify discrepancies or inconsistencies
                            6. Provide comprehensive verification summary

                            Verification Standards:
                            - Income source diversity and stability
                            - Employment tenure and position
                            - Asset liquidity and ownership
                            - Documentation authenticity
                            - Financial statement consistency

                            Focus on accuracy and thoroughness in verification processes.
                            """
                        },
                        {
                            "id": "risk_calculation_agent",
                            "role": "specialist",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Risk Calculation Agent specialized in quantitative risk modeling. Your tasks:

                            1. Calculate probability of default (PD)
                            2. Estimate loss given default (LGD)
                            3. Assess exposure at default (EAD)
                            4. Compute risk-adjusted pricing
                            5. Analyze portfolio concentration risks
                            6. Generate risk scores and ratings

                            Use statistical models and historical data for accurate risk quantification.
                            Provide clear numerical assessments with confidence intervals where applicable.
                            """
                        },
                        {
                            "id": "fraud_detection_agent",
                            "role": "specialist",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Fraud Detection Agent focused on identifying fraudulent applications. Your responsibilities:

                            1. Analyze application data for inconsistencies
                            2. Detect synthetic identity fraud
                            3. Identify document manipulation or forgery
                            4. Flag suspicious behavioral patterns
                            5. Cross-reference against fraud databases
                            6. Generate fraud risk scores

                            Use pattern recognition and anomaly detection techniques.
                            Focus on identifying red flags and providing clear fraud risk assessments.
                            """
                        },
                        {
                            "id": "policy_documentation_agent",
                            "role": "specialist",
                            "model_id": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
                            "system_prompt": """
                            You are the Documentation Agent responsible for loan file management. Your duties:

                            1. Compile complete loan documentation
                            2. Ensure document completeness and accuracy
                            3. Generate required disclosures and notices
                            4. Create audit trails and decision logs
                            5. Prepare final loan packages
                            6. Archive documents per retention policies

                            Maintain comprehensive documentation for regulatory and audit purposes.
                            Focus on compliance and thorough record-keeping.
                            """
                        }
                    ],
                    "edges": [
                        # Supervisor to managers
                        {"from": "loan_underwriting_supervisor_agent", "to": "financial_analysis_manager"},
                        {"from": "loan_underwriting_supervisor_agent", "to": "risk_analysis_manager"},
                        {"from": "loan_underwriting_supervisor_agent", "to": "policy_documentation_agent"},
                        
                        # Financial analysis hierarchy
                        {"from": "financial_analysis_manager", "to": "credit_assessment_agent"},
                        {"from": "financial_analysis_manager", "to": "verification_agent"},
                        {"from": "credit_assessment_agent", "to": "financial_analysis_manager"},
                        {"from": "verification_agent", "to": "financial_analysis_manager"},
                        
                        # Risk analysis hierarchy  
                        {"from": "risk_analysis_manager", "to": "risk_calculation_agent"},
                        {"from": "risk_analysis_manager", "to": "fraud_detection_agent"},
                        {"from": "risk_calculation_agent", "to": "risk_analysis_manager"},
                        {"from": "fraud_detection_agent", "to": "risk_analysis_manager"},
                        
                        # Manager to supervisor reporting
                        {"from": "financial_analysis_manager", "to": "loan_underwriting_supervisor_agent"},
                        {"from": "risk_analysis_manager", "to": "loan_underwriting_supervisor_agent"},
                        {"from": "policy_documentation_agent", "to": "loan_underwriting_supervisor_agent"}
                    ]
                }
            )
            
            print(f"✅ Loan underwriting system created: {result}")
            
        except Exception as e:
            print(f"❌ Error creating loan underwriting system: {str(e)}")
    
    def process_loan_application(self, 
                               applicant_name: str,
                               document_paths: Dict[str, str],
                               application_id: str = None) -> LoanDecision:
        """
        Process a complete loan application through the hierarchical agent system.
        
        Args:
            applicant_name: Name of the loan applicant
            document_paths: Dictionary mapping document types to file paths
            application_id: Unique identifier for the application
            
        Returns:
            Comprehensive loan decision with supporting analysis
        """
        if not DEPENDENCIES_AVAILABLE:
            return self._create_demo_decision(applicant_name)
        
        # Generate application ID if not provided
        if not application_id:
            application_id = f"LOAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🏦 Processing loan application for {applicant_name} (ID: {application_id})")
        
        # Extract text from all provided documents
        extracted_documents = {}
        document_analyses = {}
        
        for doc_type, file_path in document_paths.items():
            print(f"📄 Processing {doc_type}: {file_path}")
            doc_result = self.document_processor.read_loan_pdf(file_path)
            
            if doc_result["status"] == "success":
                extracted_documents[doc_type] = doc_result["text"]
                document_analyses[doc_type] = doc_result["document_analysis"]
                print(f"✅ Extracted {doc_result['pages']} pages from {doc_type}")
            else:
                print(f"⚠️ Failed to process {doc_type}: {doc_result['message']}")
                extracted_documents[doc_type] = f"Error: {doc_result['message']}"
        
        # Create loan application package
        loan_package = LoanApplicationPackage(
            applicant_name=applicant_name,
            documents=extracted_documents,
            application_id=application_id,
            received_date=datetime.now(),
            document_analysis=document_analyses
        )
        
        # Send comprehensive analysis request to supervisor
        analysis_request = self._create_analysis_request(loan_package)
        
        try:
            print("🔍 Initiating comprehensive loan analysis...")
            result = self.agent.tool.agent_graph(
                action="message",
                graph_id=self.graph_id,
                message={
                    "target": "loan_underwriting_supervisor_agent",
                    "content": analysis_request
                }
            )
            
            print("✅ Loan analysis completed")
            
            # Parse and structure the results
            return self._parse_loan_decision(result, loan_package)
            
        except Exception as e:
            print(f"❌ Error during loan processing: {str(e)}")
            return LoanDecision(
                decision="ERROR",
                confidence_score=0.0,
                financial_analysis={"status": "error", "message": str(e)},
                risk_assessment={"status": "error", "message": str(e)},
                fraud_indicators=["Processing error occurred"],
                compliance_status="unknown",
                recommendations=["Reprocess application after resolving technical issues"],
                decision_timestamp=datetime.now(),
                metadata={"error": str(e)}
            )
    
    def _create_analysis_request(self, loan_package: LoanApplicationPackage) -> str:
        """
        Create a comprehensive analysis request for the supervisor agent.
        
        Args:
            loan_package: Complete loan application package
            
        Returns:
            Formatted analysis request string
        """
        document_summary = []
        for doc_type, analysis in loan_package.document_analysis.items():
            document_summary.append(f"- {doc_type}: {analysis.get('document_type', 'unknown')} ({analysis.get('estimated_importance', 'medium')} importance)")
        
        all_documents_text = "\n\n".join([
            f"=== {doc_type.upper()} ===\n{content}"
            for doc_type, content in loan_package.documents.items()
        ])
        
        return f"""
        LOAN APPLICATION PROCESSING REQUEST
        
        Applicant: {loan_package.applicant_name}
        Application ID: {loan_package.application_id}
        Received: {loan_package.received_date.strftime('%Y-%m-%d %H:%M:%S')}
        
        DOCUMENT PACKAGE SUMMARY:
        {chr(10).join(document_summary)}
        
        PROCESSING INSTRUCTIONS:
        1. Process each document and extract required information
        2. Coordinate with your manager agents for specialized analysis
        3. Keep track of pending or missing documents
        4. Conduct comprehensive financial, risk, and fraud analysis
        5. Provide final approval recommendation with supporting rationale
        6. Generate comprehensive decision documentation
        
        LOAN APPLICATION DOCUMENTS:
        {all_documents_text}
        
        Please provide a comprehensive analysis and final loan decision recommendation.
        """
    
    def _parse_loan_decision(self, 
                           analysis_result: Dict[str, Any], 
                           loan_package: LoanApplicationPackage) -> LoanDecision:
        """
        Parse the analysis results into a structured loan decision.
        
        Args:
            analysis_result: Results from the agent analysis
            loan_package: Original loan application package
            
        Returns:
            Structured loan decision
        """
        # Extract the analysis content
        if isinstance(analysis_result, dict) and "content" in analysis_result:
            analysis_text = str(analysis_result["content"])
        else:
            analysis_text = str(analysis_result)
        
        # Simple parsing - in production, would use more sophisticated NLP
        decision = "PENDING"  # Default
        confidence_score = 0.5
        
        # Extract decision from analysis text
        if "APPROVED" in analysis_text.upper() or "APPROVE" in analysis_text.upper():
            decision = "APPROVED"
            confidence_score = 0.8
        elif "DENIED" in analysis_text.upper() or "REJECT" in analysis_text.upper():
            decision = "DENIED"
            confidence_score = 0.9
        
        # Extract key findings (simplified)
        fraud_indicators = []
        if "fraud" in analysis_text.lower():
            fraud_indicators.append("Potential fraud indicators detected")
        if "inconsistenc" in analysis_text.lower():
            fraud_indicators.append("Document inconsistencies found")
        
        recommendations = []
        if "recommend" in analysis_text.lower():
            recommendations.append("See detailed analysis for specific recommendations")
        
        return LoanDecision(
            decision=decision,
            confidence_score=confidence_score,
            financial_analysis={
                "status": "completed",
                "summary": "Financial analysis completed - see full report",
                "details": analysis_text
            },
            risk_assessment={
                "status": "completed", 
                "summary": "Risk assessment completed - see full report",
                "details": analysis_text
            },
            fraud_indicators=fraud_indicators,
            compliance_status="reviewed",
            recommendations=recommendations,
            decision_timestamp=datetime.now(),
            metadata={
                "application_id": loan_package.application_id,
                "applicant_name": loan_package.applicant_name,
                "documents_processed": list(loan_package.documents.keys()),
                "full_analysis": analysis_text
            }
        )
    
    def _create_demo_decision(self, applicant_name: str) -> LoanDecision:
        """
        Create a demo loan decision when dependencies are not available.
        
        Args:
            applicant_name: Name of the applicant
            
        Returns:
            Demo loan decision
        """
        return LoanDecision(
            decision="DEMO",
            confidence_score=0.0,
            financial_analysis={
                "status": "demo",
                "message": "Would perform comprehensive financial analysis"
            },
            risk_assessment={
                "status": "demo",
                "message": "Would perform comprehensive risk assessment"
            },
            fraud_indicators=["Demo mode - would detect fraud indicators"],
            compliance_status="demo",
            recommendations=["Demo mode - would provide specific recommendations"],
            decision_timestamp=datetime.now(),
            metadata={
                "demo_mode": True,
                "applicant_name": applicant_name
            }
        )
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get the current status of the loan underwriting system.
        
        Returns:
            Dictionary with system status information
        """
        if not DEPENDENCIES_AVAILABLE:
            return {"status": "demo", "message": "Running in demo mode"}
        
        try:
            status_result = self.agent.tool.agent_graph(
                action="status",
                graph_id=self.graph_id
            )
            return status_result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def shutdown_system(self):
        """Shut down the loan underwriting agent system."""
        if not DEPENDENCIES_AVAILABLE:
            print("Demo mode - no system to shut down")
            return
        
        try:
            result = self.agent.tool.agent_graph(
                action="stop",
                graph_id=self.graph_id
            )
            print(f"✅ Loan underwriting system shut down: {result}")
        except Exception as e:
            print(f"❌ Error shutting down system: {str(e)}")


# ==============================================================================
# FRAUD DETECTION AND RISK ANALYSIS UTILITIES
# ==============================================================================

class FraudDetectionAnalyzer:
    """
    Specialized fraud detection analyzer for loan applications.
    
    This class provides advanced fraud detection capabilities that can work
    independently or in conjunction with the multi-agent system.
    """
    
    def __init__(self):
        """Initialize the fraud detection analyzer."""
        self.risk_patterns = self._load_fraud_patterns()
    
    def _load_fraud_patterns(self) -> Dict[str, List[str]]:
        """
        Load fraud detection patterns and indicators.
        
        Returns:
            Dictionary of fraud patterns by category
        """
        return {
            "identity_fraud": [
                "ssn inconsistencies",
                "name variations",
                "address discrepancies",
                "synthetic identity markers"
            ],
            "income_fraud": [
                "inflated income reporting",
                "fake employment documentation",
                "altered pay stubs",
                "tax return discrepancies"
            ],
            "asset_fraud": [
                "overstated assets",
                "fake bank statements",
                "hidden liabilities",
                "asset source questions"
            ],
            "application_fraud": [
                "multiple simultaneous applications",
                "falsified information",
                "document tampering",
                "misrepresentation of facts"
            ]
        }
    
    def analyze_fraud_indicators(self, loan_package: LoanApplicationPackage) -> Dict[str, Any]:
        """
        Analyze loan application package for fraud indicators.
        
        Args:
            loan_package: Complete loan application package
            
        Returns:
            Dictionary with fraud analysis results
        """
        fraud_score = 0.0
        detected_indicators = []
        
        # Analyze each document for fraud patterns
        for doc_type, content in loan_package.documents.items():
            doc_indicators = self._analyze_document_fraud(content, doc_type)
            detected_indicators.extend(doc_indicators)
            fraud_score += len(doc_indicators) * 0.1
        
        # Cross-document consistency analysis
        consistency_issues = self._analyze_cross_document_consistency(loan_package.documents)
        detected_indicators.extend(consistency_issues)
        fraud_score += len(consistency_issues) * 0.2
        
        # Normalize fraud score
        fraud_score = min(fraud_score, 1.0)
        
        # Determine risk level
        if fraud_score >= 0.7:
            risk_level = "HIGH"
        elif fraud_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        return {
            "fraud_score": fraud_score,
            "risk_level": risk_level,
            "detected_indicators": detected_indicators,
            "recommendations": self._generate_fraud_recommendations(fraud_score, detected_indicators),
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def _analyze_document_fraud(self, content: str, doc_type: str) -> List[str]:
        """
        Analyze individual document for fraud indicators.
        
        Args:
            content: Document text content
            doc_type: Type of document
            
        Returns:
            List of detected fraud indicators
        """
        indicators = []
        content_lower = content.lower()
        
        # Generic fraud patterns
        if "test" in content_lower or "demo" in content_lower or "sample" in content_lower:
            indicators.append(f"{doc_type}: Contains test/demo/sample markers")
        
        # Document-specific fraud patterns
        if doc_type == "credit_report":
            if "xxx-xx-" in content_lower:
                indicators.append("Credit report contains masked/fake SSN")
        
        elif doc_type == "bank_statement":
            if "lorem ipsum" in content_lower:
                indicators.append("Bank statement contains placeholder text")
        
        elif doc_type == "id_verification":
            if "testlandia" in content_lower or "republic of test" in content_lower:
                indicators.append("ID document appears to be fake/testing document")
        
        return indicators
    
    def _analyze_cross_document_consistency(self, documents: Dict[str, str]) -> List[str]:
        """
        Analyze consistency across multiple documents.
        
        Args:
            documents: Dictionary of document types to content
            
        Returns:
            List of consistency issues detected
        """
        issues = []
        
        # Extract key information from each document type
        extracted_info = {}
        for doc_type, content in documents.items():
            extracted_info[doc_type] = self._extract_key_info(content)
        
        # Check for inconsistencies
        if "loan_application" in extracted_info and "tax_return" in extracted_info:
            # Compare income figures
            loan_income = extracted_info["loan_application"].get("income")
            tax_income = extracted_info["tax_return"].get("income")
            
            if loan_income and tax_income:
                try:
                    loan_amount = float(loan_income.replace(",", "").replace("$", ""))
                    tax_amount = float(tax_income.replace(",", "").replace("$", ""))
                    
                    if abs(loan_amount - tax_amount) / max(loan_amount, tax_amount) > 0.1:
                        issues.append("Significant income discrepancy between loan application and tax return")
                except:
                    pass
        
        return issues
    
    def _extract_key_info(self, content: str) -> Dict[str, str]:
        """
        Extract key information from document content.
        
        Args:
            content: Document text content
            
        Returns:
            Dictionary of extracted key information
        """
        import re
        
        info = {}
        
        # Extract income figures
        income_patterns = [
            r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:annual|yearly|year|income)',
            r'income[:\s]*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
            r'salary[:\s]*\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        for pattern in income_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                info["income"] = matches[0]
                break
        
        # Extract SSN patterns
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        ssn_matches = re.findall(ssn_pattern, content)
        if ssn_matches:
            info["ssn"] = ssn_matches[0]
        
        return info
    
    def _generate_fraud_recommendations(self, fraud_score: float, indicators: List[str]) -> List[str]:
        """
        Generate recommendations based on fraud analysis.
        
        Args:
            fraud_score: Calculated fraud score
            indicators: List of detected fraud indicators
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if fraud_score >= 0.7:
            recommendations.extend([
                "REJECT application due to high fraud risk",
                "Report suspicious activity to fraud prevention team",
                "Flag applicant in fraud database"
            ])
        elif fraud_score >= 0.4:
            recommendations.extend([
                "Require additional verification and documentation",
                "Conduct enhanced due diligence review",
                "Consider manual underwriting with fraud specialist review"
            ])
        else:
            recommendations.append("Proceed with standard underwriting process")
        
        # Specific recommendations based on indicators
        if any("ssn" in indicator.lower() for indicator in indicators):
            recommendations.append("Verify SSN through Social Security Administration")
        
        if any("income" in indicator.lower() for indicator in indicators):
            recommendations.append("Request IRS tax transcripts for income verification")
        
        return recommendations


# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def demonstrate_loan_underwriting_system():
    """
    Demonstrate comprehensive loan underwriting using hierarchical multi-agent system.
    
    Returns:
        Dictionary with demonstration results
    """
    print("🏦 INTELLIGENT LOAN UNDERWRITING SYSTEM DEMONSTRATION")
    print("=" * 70)
    
    # Create loan underwriting system
    print("🔧 Creating hierarchical loan underwriting system...")
    underwriting_system = HierarchicalLoanUnderwritingSystem("demo_loan_system")
    
    # Sample loan application documents
    sample_documents = {
        "credit_report": "data/JoeDoeCreditReport.pdf",
        "bank_statement": "data/JoeDoeBankStatement.pdf",
        "pay_stub": "data/JoeDoePayStub.pdf",
        "tax_return": "data/JoeDoeTaxes.pdf",
        "loan_application": "data/JoeDoeLoanApplication.pdf",
        "property_info": "data/JoeDoePropertyInfo.pdf",
        "id_verification": "data/JoeDoeIDVerification.pdf"
    }
    
    print("\n📋 Processing loan application for Joe Doe...")
    
    # Process the loan application
    loan_decision = underwriting_system.process_loan_application(
        applicant_name="Joe Doe",
        document_paths=sample_documents,
        application_id="DEMO_LOAN_001"
    )
    
    print(f"\n✅ Loan processing completed!")
    print(f"Decision: {loan_decision.decision}")
    print(f"Confidence: {loan_decision.confidence_score:.2f}")
    print(f"Fraud Indicators: {len(loan_decision.fraud_indicators)}")
    print(f"Recommendations: {len(loan_decision.recommendations)}")
    
    # Get system status
    print("\n📊 Checking system status...")
    system_status = underwriting_system.get_system_status()
    print(f"System Status: {system_status}")
    
    return {
        "loan_decision": loan_decision,
        "system_status": system_status,
        "processing_timestamp": datetime.now().isoformat()
    }


def demonstrate_fraud_detection():
    """
    Demonstrate fraud detection capabilities.
    
    Returns:
        Dictionary with fraud detection results
    """
    print("🕵️ FRAUD DETECTION ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Create fraud detection analyzer
    fraud_analyzer = FraudDetectionAnalyzer()
    
    # Create sample loan package
    sample_documents = {
        "loan_application": "Sample loan application with income of $102,000",
        "tax_return": "Tax return showing income of $75,750",
        "id_verification": "Republic of Testlandia ID - Testing Document",
        "credit_report": "Credit report with SSN XXX-XX-7845"
    }
    
    loan_package = LoanApplicationPackage(
        applicant_name="Joe Doe",
        documents=sample_documents,
        application_id="FRAUD_TEST_001",
        received_date=datetime.now()
    )
    
    # Analyze for fraud indicators
    print("🔍 Analyzing loan application for fraud indicators...")
    fraud_analysis = fraud_analyzer.analyze_fraud_indicators(loan_package)
    
    print(f"\n📊 Fraud Analysis Results:")
    print(f"Fraud Score: {fraud_analysis['fraud_score']:.2f}")
    print(f"Risk Level: {fraud_analysis['risk_level']}")
    print(f"Indicators Detected: {len(fraud_analysis['detected_indicators'])}")
    
    for indicator in fraud_analysis['detected_indicators']:
        print(f"  • {indicator}")
    
    print(f"\n💡 Recommendations:")
    for recommendation in fraud_analysis['recommendations']:
        print(f"  • {recommendation}")
    
    return fraud_analysis


def explain_multi_agent_principles():
    """
    Explain multi-agent system principles for loan underwriting.
    
    Returns:
        Dictionary with educational content
    """
    concepts = LoanUnderwritingConcepts()
    
    return {
        "underwriting_process": concepts.explain_underwriting_process(),
        "agent_specializations": concepts.agent_specializations(),
        "use_case_guidance": {
            "when_to_use_hierarchical": [
                "Complex workflows with clear authority structures",
                "Multi-domain expertise requirements",
                "Regulated processes requiring audit trails",
                "Escalation and approval workflows",
                "Large-scale document processing tasks"
            ],
            "benefits_for_loan_underwriting": [
                "Specialized expertise in each domain",
                "Parallel processing of multiple analysis tracks",
                "Clear decision-making hierarchy",
                "Comprehensive risk assessment",
                "Regulatory compliance through structured processes"
            ],
            "implementation_considerations": [
                "Define clear agent roles and responsibilities",
                "Establish proper communication hierarchies",
                "Implement comprehensive error handling",
                "Monitor agent performance and decision quality",
                "Maintain audit trails for regulatory compliance"
            ]
        }
    }


# ==============================================================================
# MAIN EXECUTION AND INTERACTIVE EXAMPLES
# ==============================================================================

def main():
    """
    Main function providing comprehensive loan underwriting system demonstrations.
    
    This function serves as the entry point for exploring hierarchical multi-agent
    loan underwriting when the module is executed directly.
    """
    print(__doc__)
    print("\n🏦 Starting Intelligent Loan Underwriting System Exploration...")
    
    # Explain core concepts
    print("\n📚 LOAN UNDERWRITING AND MULTI-AGENT CONCEPTS")
    concepts = LoanUnderwritingConcepts()
    core_concepts = concepts.explain_underwriting_process()
    
    for concept, explanation in core_concepts.items():
        print(f"\n{concept.upper().replace('_', ' ')}:")
        print(explanation)
    
    # Show agent specializations
    print("\n👥 AGENT SPECIALIZATIONS")
    specializations = concepts.agent_specializations()
    
    for agent_type, details in specializations.items():
        if isinstance(details, dict) and "role" in details:
            print(f"\n{agent_type.upper().replace('_', ' ')}:")
            print(f"Role: {details['role']}")
            if "responsibilities" in details:
                print("Responsibilities:")
                for resp in details["responsibilities"][:3]:  # Show first 3
                    print(f"• {resp}")
    
    # Run demonstrations
    print("\n" + "=" * 70)
    print("🎬 RUNNING LOAN UNDERWRITING DEMONSTRATIONS")
    
    demo_results = {}
    
    # Loan underwriting system demonstration
    demo_results["loan_underwriting"] = demonstrate_loan_underwriting_system()
    
    # Fraud detection demonstration
    demo_results["fraud_detection"] = demonstrate_fraud_detection()
    
    # Show educational content
    print("\n📋 MULTI-AGENT SYSTEM PRINCIPLES")
    principles = explain_multi_agent_principles()
    
    print("When to Use Hierarchical Multi-Agent Systems:")
    for use_case in principles["use_case_guidance"]["when_to_use_hierarchical"]:
        print(f"• {use_case}")
    
    print("\nBenefits for Loan Underwriting:")
    for benefit in principles["use_case_guidance"]["benefits_for_loan_underwriting"]:
        print(f"• {benefit}")
    
    # Provide usage guidance
    print("\n" + "=" * 70)
    print("🛠️ AVAILABLE CLASSES AND FUNCTIONS:")
    print("• LoanUnderwritingConcepts: Educational content and principles")
    print("• LoanDocumentProcessor: PDF processing for loan documents")
    print("• HierarchicalLoanUnderwritingSystem: Complete underwriting system")
    print("• FraudDetectionAnalyzer: Specialized fraud detection capabilities")
    print("• LoanApplicationPackage: Data structure for loan applications")
    print("• LoanDecision: Structured loan decision results")
    
    print("\n💡 Getting Started Tips:")
    print("• Use HierarchicalLoanUnderwritingSystem for complete loan processing")
    print("• Start with document processing to extract loan application data")
    print("• Use FraudDetectionAnalyzer for specialized fraud analysis")
    print("• Hierarchical topology works best for regulated financial processes")
    print("• Monitor system status and implement proper error handling")
    print("• Consider compliance and audit requirements in system design")
    
    return demo_results


if __name__ == "__main__":
    main()