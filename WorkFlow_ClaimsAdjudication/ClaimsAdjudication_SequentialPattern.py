#!/usr/bin/env python3
"""
Autonomous Claims Adjudication using Agent Workflows with Strands Agents

This module provides a comprehensive implementation of autonomous insurance claims adjudication
using sequential workflow patterns. It demonstrates how specialized agents can work together
in a structured sequence to process insurance claims through systematic evaluation and
decision-making processes.

The module includes:
- JSON/PDF document processing for insurance claims (FNOL)
- Sequential workflow architecture for claims adjudication
- Specialized agents for each step of the claims process
- Comprehensive fraud detection and policy verification
- Settlement calculation and final authorization workflows
- Educational examples of sequential workflow patterns
"""

import time
import json
import logging
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from datetime import datetime
import datetime as dt

# Third-party imports
try:
    import PyPDF2
    import boto3
    import yaml
    from strands import Agent, tool
    from strands.models.bedrock import BedrockModel
    from strands_tools import think, http_request, swarm, workflow
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    print("Warning: Some dependencies not available. Running in demonstration mode.")
    DEPENDENCIES_AVAILABLE = False


# ==============================================================================
# CLAIMS ADJUDICATION AND WORKFLOW CONCEPTS
# ==============================================================================

class ClaimsAdjudicationConcepts:
    """
    Educational class explaining claims adjudication processes and sequential workflow principles.
    
    This class provides comprehensive documentation of the theoretical foundations
    for building effective sequential workflow systems for insurance claims processing.
    """
    
    @staticmethod
    def explain_claims_adjudication() -> Dict[str, str]:
        """
        Explains the comprehensive claims adjudication process and its components.
        
        Returns:
            Dictionary mapping process components to detailed explanations
        """
        return {
            "claims_adjudication_overview": """
                CLAIMS ADJUDICATION PROCESS:
                Claims adjudication is the process by which insurance companies process, review, 
                validate, and assess claims to determine if they should be paid, adjusted, or denied.
                
                Key Stages:
                1. First Notice of Loss (FNOL) Processing
                   • Data extraction and validation
                   • Initial claim registration
                   • Completeness verification
                
                2. Policy Verification and Coverage Analysis
                   • Policy status validation
                   • Coverage determination
                   • Limits and deductibles assessment
                
                3. Fraud Detection and Risk Assessment
                   • Pattern analysis and anomaly detection
                   • Historical claim comparison  
                   • Risk scoring and flagging
                
                4. Damage Appraisal and Cost Estimation
                   • Comprehensive damage assessment
                   • Repair cost estimation
                   • Contractor validation
                
                5. Settlement Calculation
                   • Final payout determination
                   • Adjustments and deductions
                   • Compliance verification
                
                6. Final Review and Authorization
                   • Quality assurance checks
                   • Decision authorization
                   • Documentation completion
            """,
            
            "sequential_workflow_principles": """
                SEQUENTIAL WORKFLOW PATTERN:
                In claims adjudication, tasks have dependencies and need to be completed 
                before moving to the next task. Sequential patterns ensure proper order:
                
                • Task Dependencies: Each step builds upon previous results
                • Data Flow: Information flows sequentially through the pipeline
                • Quality Gates: Each stage validates before proceeding
                • Error Handling: Issues halt progression until resolved
                • Audit Trail: Complete history of decisions and actions
                
                Benefits:
                • Ensures proper validation at each step
                • Maintains data integrity throughout process
                • Provides clear audit trail for compliance
                • Enables quality control checkpoints
                • Supports regulatory requirements
            """,
            
            "multi_agent_workflow_benefits": """
                MULTI-AGENT WORKFLOW ADVANTAGES:
                
                Principle #1: Use Case Qualification
                • Don't force-fit workloads into collaboration patterns
                • Identify business decision frictions and design workflows around proper patterns
                
                Principle #2: Enterprise Productivity Design  
                • Use agentic systems when decision automation is needed
                • Design for enterprise productivity, not just individual task augmentation
                
                Principle #3: Acknowledge Trade-offs
                • Balance agency, control, and reliability in workflow design
                • Consider the implications of autonomous decision-making
                
                For Claims Processing:
                • Specialized expertise at each stage
                • Consistent application of business rules
                • Scalable processing of high claim volumes
                • Reduced human error and bias
                • 24/7 processing capability
                • Comprehensive documentation and audit trails
            """
        }
    
    @staticmethod
    def workflow_stage_specifications() -> Dict[str, Dict[str, Any]]:
        """
        Provides detailed specifications for each stage in the claims adjudication workflow.
        
        Returns:
            Dictionary with workflow stages and their specialized functions
        """
        return {
            "fnol_processing": {
                "role": "Claims Data Extraction Specialist",
                "purpose": "Extract, validate, and structure FNOL data with completeness checks",
                "key_activities": [
                    "Extract policy numbers, claim dates, incident details",
                    "Validate data completeness and format compliance",
                    "Structure output with confidence scores",
                    "Flag data quality issues with error codes",
                    "Generate follow-up questions for missing information"
                ],
                "quality_criteria": [
                    "All monetary amounts properly formatted",
                    "Date and identifier validation",
                    "Critical field completeness verification"
                ]
            },
            
            "policy_verification": {
                "role": "Policy Verification Specialist", 
                "purpose": "Verify policy coverage, status, and applicable terms",
                "key_activities": [
                    "Verify active coverage on incident date",
                    "Check premium payment status and policy limits",
                    "Analyze coverage applicability to incident type",
                    "Calculate maximum payout potential",
                    "Flag policy issues and exclusions"
                ],
                "decision_outcomes": [
                    "Coverage confirmed with limits",
                    "Coverage denied with policy citations",
                    "Partial coverage with restrictions"
                ]
            },
            
            "fraud_detection": {
                "role": "Fraud Detection Specialist",
                "purpose": "Analyze claim for fraud indicators and risk assessment", 
                "key_activities": [
                    "Analyze timeline and pattern inconsistencies",
                    "Assess documentation quality and authenticity",
                    "Evaluate claimant behavior indicators",
                    "Cross-reference similar claims in database",
                    "Generate risk scores and recommendations"
                ],
                "risk_levels": {
                    "LOW (0-3)": "Standard processing",
                    "MEDIUM (4-6)": "Enhanced investigation required",
                    "HIGH (7-10)": "Special Investigation Unit referral"
                }
            },
            
            "damage_appraisal": {
                "role": "Damage Appraisal Specialist",
                "purpose": "Comprehensive damage assessment and repair cost estimation",
                "key_activities": [
                    "Categorize damage by type and severity",
                    "Distinguish incident vs. pre-existing damage",
                    "Use current market rates for cost estimation",
                    "Validate contractor estimates and credentials",
                    "Document findings with detailed analysis"
                ],
                "quality_standards": [
                    "Estimates within 10% of industry standards",
                    "Clear separation of covered vs. non-covered repairs",
                    "Proper depreciation calculations"
                ]
            },
            
            "settlement_calculation": {
                "role": "Settlement Calculation Specialist",
                "purpose": "Calculate final settlement amount with all applicable adjustments",
                "key_activities": [
                    "Determine base settlement amounts",
                    "Apply deductibles and depreciation",
                    "Consider betterment and code upgrades",
                    "Validate against coverage limits",
                    "Generate payment authorization details"
                ],
                "compliance_requirements": [
                    "State regulation compliance",
                    "Company guideline adherence",
                    "Mathematical accuracy verification"
                ]
            },
            
            "final_review": {
                "role": "Final Review Specialist",
                "purpose": "Comprehensive claim review and authorization",
                "key_activities": [
                    "Verify documentation completeness",
                    "Validate specialist report consistency",
                    "Confirm regulatory compliance",
                    "Assess overall claim validity",
                    "Authorize final settlement decision"
                ],
                "decision_outcomes": [
                    "APPROVE: Issue payment with conditions",
                    "DENY: Provide detailed denial reasoning",
                    "INVESTIGATE: Refer for additional investigation"
                ]
            }
        }


# ==============================================================================
# DOCUMENT PROCESSING FOR INSURANCE CLAIMS
# ==============================================================================

class ClaimsDocumentProcessor:
    """
    Specialized processor for insurance claims documents and FNOL data.
    
    This class provides functionality to extract and prepare claims-related documents
    for analysis by workflow agents, with specific focus on First Notice of Loss (FNOL)
    forms, policy documents, and supporting claim materials.
    """
    
    @staticmethod
    def read_claims_file(file_path: str) -> Dict[str, Any]:
        """
        Read and extract data from various claims document formats.
        
        Args:
            file_path: Path to the claims document (JSON, PDF, etc.)
            
        Returns:
            Dictionary containing extracted data, metadata, and document information
        """
        try:
            if not DEPENDENCIES_AVAILABLE:
                return {
                    "status": "demo",
                    "message": "Dependencies not available - running in demo mode",
                    "data": {"demo": "Claims document content would be extracted here"},
                    "document_type": "claims_document"
                }
            
            # Determine file type and process accordingly
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'json':
                return ClaimsDocumentProcessor._read_json_file(file_path)
            elif file_extension == 'pdf':
                return ClaimsDocumentProcessor._read_pdf_file(file_path)
            else:
                return ClaimsDocumentProcessor._read_text_file(file_path)
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing claims document: {str(e)}",
                "data": {},
                "document_type": "unknown"
            }
    
    @staticmethod
    def _read_json_file(file_path: str) -> Dict[str, Any]:
        """Read JSON file containing structured claims data."""
        try:
            with open(file_path, 'r') as file:
                json_data = json.loads(file.read())
            
            # Analyze the JSON structure
            document_analysis = ClaimsDocumentProcessor._analyze_claims_data(json_data, "json")
            
            return {
                "status": "success",
                "data": json_data,
                "file_path": file_path,
                "document_type": document_analysis.get("document_type", "json_claims"),
                "document_analysis": document_analysis
            }
            
        except json.JSONDecodeError as e:
            return {
                "status": "error",
                "message": f"Invalid JSON format: {str(e)}",
                "data": {},
                "document_type": "invalid_json"
            }
    
    @staticmethod
    def _read_pdf_file(file_path: str) -> Dict[str, Any]:
        """Read PDF file containing claims documentation."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from all pages
                full_text = ""
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    full_text += page.extract_text() + "\n\n"
            
            # Analyze the PDF content
            document_analysis = ClaimsDocumentProcessor._analyze_claims_data(full_text, "pdf")
            
            return {
                "status": "success",
                "data": {"text_content": full_text, "pages": num_pages},
                "file_path": file_path,
                "document_type": document_analysis.get("document_type", "pdf_claims"),
                "document_analysis": document_analysis
            }
            
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Error reading PDF: {str(e)}",
                "data": {},
                "document_type": "pdf_error"
            }
    
    @staticmethod
    def _read_text_file(file_path: str) -> Dict[str, Any]:
        """Read text file containing claims information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read()
            
            # Analyze the text content
            document_analysis = ClaimsDocumentProcessor._analyze_claims_data(text_content, "text")
            
            return {
                "status": "success",
                "data": {"text_content": text_content},
                "file_path": file_path,
                "document_type": document_analysis.get("document_type", "text_claims"),
                "document_analysis": document_analysis
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error reading text file: {str(e)}",
                "data": {},
                "document_type": "text_error"
            }
    
    @staticmethod
    def _analyze_claims_data(data: Union[Dict, str], file_type: str) -> Dict[str, Any]:
        """
        Analyze claims data to identify document type and key characteristics.
        
        Args:
            data: The extracted data (dict for JSON, string for text/PDF)
            file_type: Type of source file
            
        Returns:
            Dictionary with document analysis results
        """
        analysis = {
            "document_type": "unknown_claims",
            "contains_fnol_data": False,
            "contains_policy_info": False,
            "contains_financial_data": False,
            "estimated_completeness": "unknown"
        }
        
        if isinstance(data, dict):
            # Analyze JSON structure
            keys = str(data.keys()).lower()
            values = str(data.values()).lower()
            content = keys + " " + values
        else:
            # Analyze text content
            content = str(data).lower()
        
        # Document type detection
        if any(indicator in content for indicator in ["fnol", "first notice", "loss notification"]):
            analysis["document_type"] = "fnol"
            analysis["contains_fnol_data"] = True
        elif any(indicator in content for indicator in ["policy", "coverage", "deductible"]):
            analysis["document_type"] = "policy_document"
            analysis["contains_policy_info"] = True
        elif any(indicator in content for indicator in ["claim", "incident", "damage"]):
            analysis["document_type"] = "claim_document"
        
        # Data completeness assessment
        financial_indicators = ["amount", "cost", "estimate", "payment", "settlement"]
        if any(indicator in content for indicator in financial_indicators):
            analysis["contains_financial_data"] = True
        
        # Estimate completeness
        critical_fields = ["policy", "date", "incident", "amount", "claimant"]
        present_fields = sum(1 for field in critical_fields if field in content)
        
        if present_fields >= 4:
            analysis["estimated_completeness"] = "high"
        elif present_fields >= 2:
            analysis["estimated_completeness"] = "medium"
        else:
            analysis["estimated_completeness"] = "low"
        
        return analysis


# ==============================================================================
# SEQUENTIAL CLAIMS ADJUDICATION WORKFLOW SYSTEM
# ==============================================================================

@dataclass
class ClaimsWorkflowResult:
    """
    Container for claims workflow execution results.
    
    Attributes:
        workflow_id: Unique identifier for the workflow execution
        claim_id: Identifier for the processed claim
        final_decision: Final adjudication decision
        settlement_amount: Calculated settlement amount (if approved)
        processing_stages: Results from each workflow stage
        execution_time: Total processing time
        completion_timestamp: When workflow completed
    """
    workflow_id: str
    claim_id: str
    final_decision: str
    settlement_amount: Optional[float]
    processing_stages: Dict[str, Any]
    execution_time: float
    completion_timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


class SequentialClaimsAdjudicationSystem:
    """
    Comprehensive claims adjudication system using sequential workflow architecture.
    
    This class creates and manages a sequential workflow of specialized agents
    to process insurance claims through systematic evaluation stages from FNOL
    processing through final settlement authorization.
    """
    
    def __init__(self, workflow_id: str = "claims_adjudication_workflow"):
        """Initialize the sequential claims adjudication system."""
        self.workflow_id = workflow_id
        self.document_processor = ClaimsDocumentProcessor()
        
        if DEPENDENCIES_AVAILABLE:
            self.agent = Agent(tools=[workflow])
            self._create_claims_workflow()
        else:
            print("Running in demo mode - Strands not available")
            self.agent = None
    
    def _create_claims_workflow(self):
        """Create the sequential workflow for claims adjudication."""
        try:
            result = self.agent.tool.workflow(
                action="create",
                workflow_id=self.workflow_id,
                tasks=[
                    {
                        "task_id": "fnol_processing",
                        "description": "Extract, validate, and structure FNOL data with completeness checks",
                        "system_prompt": """You are a Claims Data Extraction Specialist.

                        ROLE: Process First Notice of Loss (FNOL) forms and extract structured claim data.
                        
                        INPUTS: Raw FNOL document/form data 
                        OUTPUTS: Structured JSON with validated claim information
                        
                        INSTRUCTIONS:
                        1. Extract key data points:
                           - Policy number, claim date, incident location, claimant details
                           - Incident description, damages reported, witnesses
                           - Supporting documentation references
                        
                        2. Validate data completeness:
                           - Flag missing required fields
                           - Identify inconsistencies in dates/locations
                           - Check format compliance (policy numbers, contact info)
                        
                        3. Structure output as JSON with confidence scores for each field
                        4. Flag potential data quality issues with specific error codes
                        5. If critical information is missing, generate specific follow-up questions
                        
                        ERROR HANDLING: If form is illegible or severely incomplete, flag for manual review with detailed reasoning.
                        
                        QUALITY CHECK: Ensure all extracted monetary amounts, dates, and identifiers are properly formatted.""",
                        "priority": 5
                    },
                    
                    {
                        "task_id": "policy_verification",
                        "description": "Verify policy coverage, status, and applicable terms",
                        "dependencies": ["fnol_processing"],
                        "system_prompt": """You are a Policy Verification Specialist.

                        ROLE: Validate policy coverage and determine claim eligibility.
                        
                        INPUTS: Structured claim data, policy database access
                        OUTPUTS: Policy verification report with coverage determination
                        
                        INSTRUCTIONS:
                        1. Verify policy status:
                           - Active coverage on incident date
                           - Premium payment status
                           - Policy limits and deductibles
                        
                        2. Analyze coverage applicability:
                           - Match incident type to covered perils
                           - Check for exclusions or limitations
                           - Identify applicable sub-limits
                        
                        3. Calculate coverage amounts:
                           - Maximum payout potential
                           - Deductible applications
                           - Co-insurance factors
                        
                        4. Flag policy issues:
                           - Lapsed coverage, exclusions, fraud indicators
                           - Material misrepresentation concerns
                        
                        OUTPUT FORMAT: Structured report with coverage determination, limits, and any red flags.
                        
                        DECISION LOGIC: If policy is invalid or claim not covered, provide clear denial reasoning with policy section references.""",
                        "priority": 4
                    },

                    {
                        "task_id": "fraud_detection",
                        "description": "Analyze claim for fraud indicators and risk assessment",
                        "dependencies": ["fnol_processing"],
                        "system_prompt": """You are a Fraud Detection Specialist.

                        ROLE: Identify potential fraud indicators and assess claim authenticity.
                        
                        INPUTS: Claim data, historical patterns, external data sources
                        OUTPUTS: Fraud risk assessment with detailed analysis
                        
                        FRAUD INDICATORS TO ANALYZE:
                        1. Timeline inconsistencies (reporting delays, convenient timing)
                        2. Claim patterns (frequency, amounts, incident types)
                        3. Documentation quality (photos, estimates, witness statements)
                        4. Claimant behavior (evasiveness, excessive pressure, coaching signs)
                        5. Damage consistency (impact patterns, wear indicators)
                        
                        RISK SCORING:
                        - LOW (0-3): Standard processing
                        - MEDIUM (4-6): Enhanced investigation required
                        - HIGH (7-10): Special Investigation Unit referral
                        
                        ANALYSIS REQUIREMENTS:
                        - Cross-reference similar claims in database
                        - Verify incident location and timing plausibility
                        - Assess damage patterns against reported cause
                        - Check for staging indicators
                        
                        OUTPUT: Risk score with specific indicators found and recommended actions.""",
                        "priority": 4
                    },

                    {
                        "task_id": "damage_appraisal",
                        "description": "Comprehensive damage assessment and repair cost estimation",
                        "dependencies": ["policy_verification", "fraud_detection"],
                        "system_prompt": """You are a Damage Appraisal Specialist.

                        ROLE: Conduct thorough damage assessment and provide accurate repair cost estimates.
                        
                        INPUTS: Claim details, photos, estimates, policy coverage info
                        OUTPUTS: Detailed appraisal report with itemized repair costs
                        
                        APPRAISAL PROCESS:
                        1. Damage Analysis:
                           - Categorize damage by type and severity
                           - Distinguish pre-existing vs. incident-related damage
                           - Assess structural vs. cosmetic damage
                        
                        2. Cost Estimation:
                           - Use current market rates for materials/labor
                           - Consider regional cost variations
                           - Factor in quality/grade matching requirements
                           - Include necessary vs. improvement upgrades
                        
                        3. Validation Steps:
                           - Compare submitted estimates with market standards
                           - Verify contractor credentials and estimates
                           - Check for inflated or unnecessary repairs
                        
                        4. Documentation:
                           - Detailed photo analysis with annotations
                           - Line-item cost breakdown
                           - Justification for any estimate adjustments
                        
                        QUALITY STANDARDS:
                        - All estimates within 10% industry standard ranges
                        - Clear separation of covered vs. non-covered repairs
                        - Depreciation calculations where applicable
                        
                        RED FLAGS: Identify overpriced estimates, unnecessary repairs, or non-incident damage claims.""",
                        "priority": 3
                    },

                    {
                        "task_id": "settlement_calculation",
                        "description": "Calculate final settlement amount with all applicable adjustments",
                        "dependencies": ["damage_appraisal"],
                        "system_prompt": """You are a Settlement Calculation Specialist.

                        ROLE: Determine final claim payout with precise calculations and proper adjustments.
                        
                        INPUTS: Appraisal report, policy terms, coverage verification
                        OUTPUTS: Final settlement calculation with detailed breakdown
                        
                        CALCULATION COMPONENTS:
                        1. Base Settlement:
                           - Approved repair costs
                           - Replacement cost vs. actual cash value
                           - Applicable coverage limits
                        
                        2. Adjustments:
                           - Deductible applications
                           - Depreciation calculations
                           - Betterment considerations
                           - Sales tax implications
                        
                        3. Additional Considerations:
                           - Loss of use/additional living expenses
                           - Code upgrade requirements
                           - Salvage value deductions
                        
                        VERIFICATION REQUIREMENTS:
                        - Double-check all mathematical calculations
                        - Ensure compliance with policy terms
                        - Validate against coverage limits
                        - Confirm proper deductible application
                        
                        OUTPUT FORMAT:
                        - Settlement summary with line-item breakdown
                        - Payment authorization details
                        - Required documentation for disbursement
                        - Any conditions or requirements for payment
                        
                        COMPLIANCE: Ensure all calculations comply with state regulations and company guidelines.""",
                        "priority": 2
                    },

                    {
                        "task_id": "final_review",
                        "description": "Comprehensive claim review and authorization",
                        "dependencies": ["settlement_calculation"],
                        "system_prompt": """You are a Final Review Specialist.

                        ROLE: Conduct final quality assurance and authorize claim settlement.
                        
                        INPUTS: Complete claim file with all specialist reports
                        OUTPUTS: Final authorization decision with comprehensive summary
                        
                        REVIEW CHECKLIST:
                        1. Completeness Verification:
                           - All required documentation present
                           - Specialist reports consistent and logical
                           - No outstanding information gaps
                        
                        2. Accuracy Validation:
                           - Settlement calculations verified
                           - Policy applications correct
                           - Fraud assessment reasonable
                        
                        3. Compliance Check:
                           - Regulatory requirements met
                           - Company guidelines followed
                           - Proper authorization levels
                        
                        4. Risk Assessment:
                           - Overall claim validity confirmed
                           - Appropriate settlement amount
                           - No unresolved red flags
                        
                        DECISION OUTCOMES:
                        - APPROVE: Issue payment with conditions specified
                        - DENY: Provide detailed denial reasoning with policy citations
                        - INVESTIGATE: Refer for additional investigation with specific requirements
                        
                        DOCUMENTATION: Create comprehensive claim summary for audit trail and future reference.
                        
                        ESCALATION: Flag any claims exceeding authority limits or requiring special handling.""",
                        "priority": 1
                    }
                ]
            )
            
            print(f"✅ Claims adjudication workflow created: {result}")
            
        except Exception as e:
            print(f"❌ Error creating claims workflow: {str(e)}")
    
    def process_claim(self, 
                     claim_data_path: str,
                     claim_id: str = None) -> ClaimsWorkflowResult:
        """
        Process an insurance claim through the sequential adjudication workflow.
        
        Args:
            claim_data_path: Path to the FNOL or claims data file
            claim_id: Unique identifier for the claim
            
        Returns:
            Comprehensive workflow execution results
        """
        if not DEPENDENCIES_AVAILABLE:
            return self._create_demo_result(claim_id or "DEMO_CLAIM")
        
        # Generate claim ID if not provided
        if not claim_id:
            claim_id = f"CLAIM_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🏥 Processing insurance claim: {claim_id}")
        
        # Load and process the claims data
        print(f"📄 Loading claims data from: {claim_data_path}")
        claims_data = self.document_processor.read_claims_file(claim_data_path)
        
        if claims_data["status"] != "success":
            print(f"❌ Failed to process claims data: {claims_data['message']}")
            return ClaimsWorkflowResult(
                workflow_id=self.workflow_id,
                claim_id=claim_id,
                final_decision="ERROR",
                settlement_amount=None,
                processing_stages={"error": claims_data},
                execution_time=0.0,
                completion_timestamp=datetime.now(),
                metadata={"error": "Failed to process input data"}
            )
        
        print(f"✅ Claims data loaded: {claims_data['document_type']}")
        
        # Start workflow execution
        start_time = time.time()
        
        try:
            print("🔄 Starting sequential claims adjudication workflow...")
            
            # Start the workflow with claims data
            workflow_result = self.agent.tool.workflow(
                action="start",
                workflow_id=self.workflow_id,
                input_data=claims_data["data"]
            )
            
            # Check workflow status
            status_result = self.agent.tool.workflow(
                action="status", 
                workflow_id=self.workflow_id
            )
            
            execution_time = time.time() - start_time
            
            print(f"✅ Workflow completed in {execution_time:.2f} seconds")
            
            # Parse workflow results
            return self._parse_workflow_results(
                workflow_result,
                status_result, 
                claim_id,
                execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Error during workflow execution: {str(e)}")
            
            return ClaimsWorkflowResult(
                workflow_id=self.workflow_id,
                claim_id=claim_id,
                final_decision="ERROR",
                settlement_amount=None,
                processing_stages={"error": str(e)},
                execution_time=execution_time,
                completion_timestamp=datetime.now(),
                metadata={"error": "Workflow execution failed"}
            )
    
    def _parse_workflow_results(self,
                              workflow_result: Dict[str, Any],
                              status_result: Dict[str, Any], 
                              claim_id: str,
                              execution_time: float) -> ClaimsWorkflowResult:
        """
        Parse workflow execution results into structured format.
        
        Args:
            workflow_result: Results from workflow execution
            status_result: Status information from workflow
            claim_id: Claim identifier
            execution_time: Total execution time
            
        Returns:
            Structured workflow results
        """
        # Extract final decision and settlement amount
        final_decision = "PENDING"  # Default
        settlement_amount = None
        processing_stages = {}
        
        # Parse workflow results (simplified parsing)
        if isinstance(workflow_result, dict):
            if "content" in workflow_result:
                content = str(workflow_result["content"])
                
                # Extract decision
                if "APPROVE" in content.upper():
                    final_decision = "APPROVED"
                elif "DENY" in content.upper():
                    final_decision = "DENIED"
                elif "INVESTIGATE" in content.upper():
                    final_decision = "INVESTIGATE"
                
                # Extract settlement amount (simplified)
                import re
                amount_matches = re.findall(r'\$[\d,]+\.?\d*', content)
                if amount_matches:
                    try:
                        settlement_amount = float(amount_matches[-1].replace('$', '').replace(',', ''))
                    except:
                        pass
        
        # Extract stage information from status
        if isinstance(status_result, dict):
            processing_stages = status_result
        
        return ClaimsWorkflowResult(
            workflow_id=self.workflow_id,
            claim_id=claim_id,
            final_decision=final_decision,
            settlement_amount=settlement_amount,
            processing_stages=processing_stages,
            execution_time=execution_time,
            completion_timestamp=datetime.now(),
            metadata={
                "workflow_result": workflow_result,
                "status_result": status_result
            }
        )
    
    def _create_demo_result(self, claim_id: str) -> ClaimsWorkflowResult:
        """
        Create demo workflow result when dependencies are not available.
        
        Args:
            claim_id: Claim identifier
            
        Returns:
            Demo workflow result
        """
        return ClaimsWorkflowResult(
            workflow_id=self.workflow_id,
            claim_id=claim_id,
            final_decision="DEMO",
            settlement_amount=15000.00,
            processing_stages={
                "fnol_processing": "Demo: Would extract and validate FNOL data",
                "policy_verification": "Demo: Would verify policy coverage",
                "fraud_detection": "Demo: Would analyze fraud indicators",
                "damage_appraisal": "Demo: Would assess damage and costs",
                "settlement_calculation": "Demo: Would calculate settlement",
                "final_review": "Demo: Would conduct final review"
            },
            execution_time=0.0,
            completion_timestamp=datetime.now(),
            metadata={"demo_mode": True}
        )
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """
        Get the current status of the claims adjudication workflow.
        
        Returns:
            Dictionary with workflow status information
        """
        if not DEPENDENCIES_AVAILABLE:
            return {"status": "demo", "message": "Running in demo mode"}
        
        try:
            status_result = self.agent.tool.workflow(
                action="status",
                workflow_id=self.workflow_id
            )
            return status_result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def stop_workflow(self):
        """Stop the claims adjudication workflow."""
        if not DEPENDENCIES_AVAILABLE:
            print("Demo mode - no workflow to stop")
            return
        
        try:
            result = self.agent.tool.workflow(
                action="stop",
                workflow_id=self.workflow_id
            )
            print(f"✅ Claims workflow stopped: {result}")
        except Exception as e:
            print(f"❌ Error stopping workflow: {str(e)}")


# ==============================================================================
# FRAUD DETECTION AND RISK ANALYSIS UTILITIES
# ==============================================================================

class ClaimsFraudAnalyzer:
    """
    Specialized fraud detection analyzer for insurance claims.
    
    This class provides advanced fraud detection capabilities that can work
    independently or in conjunction with the sequential workflow system.
    """
    
    def __init__(self):
        """Initialize the claims fraud analyzer."""
        self.fraud_patterns = self._load_fraud_patterns()
    
    def _load_fraud_patterns(self) -> Dict[str, List[str]]:
        """
        Load fraud detection patterns and indicators for claims.
        
        Returns:
            Dictionary of fraud patterns by category
        """
        return {
            "timeline_fraud": [
                "Late reporting without valid reason",
                "Incident timing coincides with financial stress",
                "Convenient timing near policy expiration",
                "Weekend/holiday incident reporting patterns"
            ],
            "documentation_fraud": [
                "Poor quality photos or videos",
                "Missing or incomplete documentation", 
                "Altered or manipulated documents",
                "Inconsistent damage documentation"
            ],
            "behavioral_fraud": [
                "Evasive responses to questions",
                "Excessive pressure for quick settlement",
                "Unusual knowledge of claims process",
                "Reluctance to provide additional information"
            ],
            "damage_fraud": [
                "Damage inconsistent with reported cause",
                "Pre-existing damage claimed as new",
                "Staged accident indicators",
                "Inflated damage assessments"
            ]
        }
    
    def analyze_claim_fraud_risk(self, claims_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze claims data for fraud indicators and risk assessment.
        
        Args:
            claims_data: Complete claims data for analysis
            
        Returns:
            Dictionary with fraud risk analysis results
        """
        fraud_score = 0.0
        detected_indicators = []
        risk_factors = []
        
        # Convert claims data to searchable text
        claims_text = json.dumps(claims_data).lower()
        
        # Analyze for each fraud pattern category
        for category, patterns in self.fraud_patterns.items():
            category_indicators = []
            
            for pattern in patterns:
                if self._pattern_matches(pattern, claims_text, claims_data):
                    category_indicators.append(pattern)
                    detected_indicators.append(f"{category}: {pattern}")
            
            if category_indicators:
                risk_factors.append({
                    "category": category,
                    "indicators": category_indicators,
                    "risk_weight": len(category_indicators) * 0.15
                })
                fraud_score += len(category_indicators) * 0.15
        
        # Additional risk factors based on data patterns
        additional_risks = self._analyze_data_patterns(claims_data)
        risk_factors.extend(additional_risks)
        fraud_score += sum(risk["risk_weight"] for risk in additional_risks)
        
        # Normalize fraud score
        fraud_score = min(fraud_score, 1.0)
        
        # Determine risk level
        if fraud_score >= 0.7:
            risk_level = "HIGH"
            recommended_action = "Special Investigation Unit referral"
        elif fraud_score >= 0.4:
            risk_level = "MEDIUM"
            recommended_action = "Enhanced investigation required"
        else:
            risk_level = "LOW"
            recommended_action = "Standard processing"
        
        return {
            "fraud_score": fraud_score,
            "risk_level": risk_level,
            "detected_indicators": detected_indicators,
            "risk_factors": risk_factors,
            "recommended_action": recommended_action,
            "analysis_timestamp": datetime.now().isoformat(),
            "fraud_analysis_summary": self._generate_fraud_summary(fraud_score, risk_factors)
        }
    
    def _pattern_matches(self, pattern: str, claims_text: str, claims_data: Dict) -> bool:
        """
        Check if a fraud pattern matches the claims data.
        
        Args:
            pattern: Fraud pattern to check
            claims_text: Claims data as searchable text
            claims_data: Structured claims data
            
        Returns:
            Boolean indicating if pattern matches
        """
        # Simple keyword-based matching (would be more sophisticated in production)
        pattern_keywords = pattern.lower().split()
        return any(keyword in claims_text for keyword in pattern_keywords[:2])
    
    def _analyze_data_patterns(self, claims_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze claims data for additional fraud patterns.
        
        Args:
            claims_data: Structured claims data
            
        Returns:
            List of additional risk factors found
        """
        additional_risks = []
        
        # Check for missing critical information
        critical_fields = ["policy_number", "incident_date", "claimant_name", "damage_amount"]
        missing_fields = []
        
        claims_text = json.dumps(claims_data).lower()
        for field in critical_fields:
            if field.replace("_", " ") not in claims_text and field not in claims_text:
                missing_fields.append(field)
        
        if missing_fields:
            additional_risks.append({
                "category": "data_completeness",
                "indicators": [f"Missing critical field: {field}" for field in missing_fields],
                "risk_weight": len(missing_fields) * 0.1
            })
        
        # Check for suspicious amounts
        try:
            # Look for amount patterns in the data
            import re
            amounts = re.findall(r'\d+\.?\d*', json.dumps(claims_data))
            if amounts:
                numeric_amounts = [float(a) for a in amounts if float(a) > 1000]
                if numeric_amounts:
                    max_amount = max(numeric_amounts)
                    if max_amount > 50000:  # High value claim
                        additional_risks.append({
                            "category": "high_value_claim",
                            "indicators": [f"High value claim: ${max_amount:,.2f}"],
                            "risk_weight": 0.2
                        })
        except:
            pass
        
        return additional_risks
    
    def _generate_fraud_summary(self, fraud_score: float, risk_factors: List[Dict]) -> str:
        """
        Generate a comprehensive fraud analysis summary.
        
        Args:
            fraud_score: Calculated fraud score
            risk_factors: List of identified risk factors
            
        Returns:
            Formatted fraud analysis summary
        """
        summary = f"Fraud Risk Analysis Summary (Score: {fraud_score:.2f}/1.0)\n"
        summary += "=" * 50 + "\n\n"
        
        for factor in risk_factors:
            summary += f"{factor['category'].upper().replace('_', ' ')}:\n"
            for indicator in factor['indicators']:
                summary += f"  • {indicator}\n"
            summary += f"  Risk Weight: {factor['risk_weight']:.2f}\n\n"
        
        if fraud_score >= 0.7:
            summary += "RECOMMENDATION: Immediate Special Investigation Unit review required."
        elif fraud_score >= 0.4:
            summary += "RECOMMENDATION: Enhanced investigation and additional documentation required."
        else:
            summary += "RECOMMENDATION: Proceed with standard claims processing."
        
        return summary


# ==============================================================================
# DEMONSTRATION AND EXAMPLES
# ==============================================================================

def demonstrate_claims_adjudication_workflow():
    """
    Demonstrate comprehensive claims adjudication using sequential workflow.
    
    Returns:
        Dictionary with demonstration results
    """
    print("🏥 AUTONOMOUS CLAIMS ADJUDICATION WORKFLOW DEMONSTRATION")
    print("=" * 70)
    
    # Create claims adjudication system
    print("🔧 Creating sequential claims adjudication workflow...")
    adjudication_system = SequentialClaimsAdjudicationSystem("demo_claims_workflow")
    
    # Sample FNOL data path (would be actual file in real implementation)
    sample_fnol_path = "data/FNOL.json"
    
    # Create sample FNOL data for demo
    sample_fnol_data = {
        "claim_number": "CLM-2024-001234",
        "policy_number": "POL-987654321",
        "incident_date": "2024-01-15",
        "report_date": "2024-01-16",
        "claimant": {
            "name": "John Smith",
            "phone": "555-0123",
            "email": "john.smith@email.com"
        },
        "incident": {
            "type": "auto_accident",
            "location": "123 Main St, Anytown, ST 12345",
            "description": "Rear-end collision at traffic light",
            "weather": "clear",
            "estimated_damage": 8500.00
        },
        "policy": {
            "type": "auto",
            "deductible": 500.00,
            "limits": {"property_damage": 25000.00}
        }
    }
    
    # Save sample data to temporary file for demo
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        json.dump(sample_fnol_data, temp_file)
        temp_fnol_path = temp_file.name
    
    print(f"\n📋 Processing sample insurance claim...")
    
    try:
        # Process the claim through workflow
        workflow_result = adjudication_system.process_claim(
            claim_data_path=temp_fnol_path,
            claim_id="DEMO_CLAIM_001"
        )
        
        print(f"\n✅ Claims processing completed!")
        print(f"Claim ID: {workflow_result.claim_id}")
        print(f"Final Decision: {workflow_result.final_decision}")
        if workflow_result.settlement_amount:
            print(f"Settlement Amount: ${workflow_result.settlement_amount:,.2f}")
        print(f"Processing Time: {workflow_result.execution_time:.2f} seconds")
        print(f"Stages Processed: {len(workflow_result.processing_stages)}")
        
        # Get workflow status
        print("\n📊 Checking workflow status...")
        workflow_status = adjudication_system.get_workflow_status()
        print(f"Workflow Status: {workflow_status}")
        
        # Clean up temporary file 
        os.unlink(temp_fnol_path)
        
        return {
            "workflow_result": workflow_result,
            "workflow_status": workflow_status,
            "sample_data": sample_fnol_data
        }
        
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        return {"error": str(e)}


def demonstrate_fraud_detection():
    """
    Demonstrate fraud detection capabilities for claims.
    
    Returns:
        Dictionary with fraud detection results
    """
    print("🕵️ CLAIMS FRAUD DETECTION DEMONSTRATION")
    print("=" * 60)
    
    # Create fraud detection analyzer
    fraud_analyzer = ClaimsFraudAnalyzer()
    
    # Sample claims data with potential fraud indicators
    suspicious_claims_data = {
        "claim_number": "CLM-2024-FRAUD",
        "policy_number": "POL-123456789",
        "incident_date": "2024-01-01",  # New Year's Day - suspicious timing
        "report_date": "2024-01-15",    # Two week delay
        "claimant": {
            "name": "Suspicious Claimant",
            "phone": "555-FAKE",
            "behavior_notes": "Evasive responses, excessive pressure for settlement"
        },
        "incident": {
            "type": "theft",
            "location": "Unknown location",
            "description": "Expensive items stolen",
            "estimated_damage": 75000.00,  # High value
            "documentation": "Poor quality photos provided"
        },
        "red_flags": [
            "Late reporting without explanation",
            "Convenient timing",
            "High value claim",
            "Poor documentation quality"
        ]
    }
    
    print("🔍 Analyzing suspicious claims data for fraud indicators...")
    fraud_analysis = fraud_analyzer.analyze_claim_fraud_risk(suspicious_claims_data)
    
    print(f"\n📊 Fraud Analysis Results:")
    print(f"Fraud Score: {fraud_analysis['fraud_score']:.2f}/1.0")
    print(f"Risk Level: {fraud_analysis['risk_level']}")
    print(f"Recommended Action: {fraud_analysis['recommended_action']}")
    
    print(f"\n🚨 Detected Indicators ({len(fraud_analysis['detected_indicators'])}):")
    for indicator in fraud_analysis['detected_indicators']:
        print(f"  • {indicator}")
    
    print(f"\n📋 Risk Factors:")
    for factor in fraud_analysis['risk_factors']:
        print(f"  • {factor['category'].replace('_', ' ').title()}: {len(factor['indicators'])} indicators")
    
    print(f"\n📄 Fraud Analysis Summary:")
    print(fraud_analysis['fraud_analysis_summary'])
    
    return fraud_analysis


def explain_sequential_workflow_principles():
    """
    Explain sequential workflow principles for claims adjudication.
    
    Returns:
        Dictionary with educational content
    """
    concepts = ClaimsAdjudicationConcepts()
    
    return {
        "adjudication_process": concepts.explain_claims_adjudication(),
        "workflow_stages": concepts.workflow_stage_specifications(),
        "implementation_guidance": {
            "when_to_use_sequential": [
                "Processes with clear task dependencies",
                "Quality gates required between stages",
                "Regulatory compliance workflows",
                "Complex multi-step decision processes",
                "Audit trail requirements"
            ],
            "benefits_for_claims": [
                "Systematic evaluation at each stage",
                "Quality control checkpoints",
                "Complete audit trail for compliance",
                "Consistent application of business rules",
                "Reduced processing errors and omissions"
            ],
            "design_considerations": [
                "Define clear stage dependencies",
                "Implement proper error handling and rollback",
                "Design for scalability and throughput",
                "Monitor performance and bottlenecks",
                "Ensure regulatory compliance at each stage"
            ]
        }
    }


# ==============================================================================
# MAIN EXECUTION AND INTERACTIVE EXAMPLES
# ==============================================================================

def main():
    """
    Main function providing comprehensive claims adjudication workflow demonstrations.
    
    This function serves as the entry point for exploring sequential workflow
    systems for insurance claims processing when the module is executed directly.
    """
    print(__doc__)
    print("\n🏥 Starting Autonomous Claims Adjudication System Exploration...")
    
    # Explain core concepts
    print("\n📚 CLAIMS ADJUDICATION AND WORKFLOW CONCEPTS")
    concepts = ClaimsAdjudicationConcepts()
    core_concepts = concepts.explain_claims_adjudication()
    
    for concept, explanation in core_concepts.items():
        print(f"\n{concept.upper().replace('_', ' ')}:")
        print(explanation)
    
    # Show workflow stage specifications
    print("\n🔧 WORKFLOW STAGE SPECIFICATIONS")
    stages = concepts.workflow_stage_specifications()
    
    for stage_id, details in stages.items():
        print(f"\n{stage_id.upper().replace('_', ' ')}:")
        print(f"Role: {details['role']}")
        print(f"Purpose: {details['purpose']}")
        if "key_activities" in details:
            print("Key Activities:")
            for activity in details["key_activities"][:3]:  # Show first 3
                print(f"• {activity}")
    
    # Run demonstrations
    print("\n" + "=" * 70)
    print("🎬 RUNNING CLAIMS ADJUDICATION DEMONSTRATIONS")
    
    demo_results = {}
    
    # Claims adjudication workflow demonstration
    demo_results["claims_workflow"] = demonstrate_claims_adjudication_workflow()
    
    # Fraud detection demonstration
    demo_results["fraud_detection"] = demonstrate_fraud_detection()
    
    # Show educational content
    print("\n📋 SEQUENTIAL WORKFLOW PRINCIPLES")
    principles = explain_sequential_workflow_principles()
    
    print("When to Use Sequential Workflows:")
    for use_case in principles["implementation_guidance"]["when_to_use_sequential"]:
        print(f"• {use_case}")
    
    print("\nBenefits for Claims Processing:")
    for benefit in principles["implementation_guidance"]["benefits_for_claims"]:
        print(f"• {benefit}")
    
    # Provide usage guidance
    print("\n" + "=" * 70)
    print("🛠️ AVAILABLE CLASSES AND FUNCTIONS:")
    print("• ClaimsAdjudicationConcepts: Educational content and principles")
    print("• ClaimsDocumentProcessor: Document processing for claims data")
    print("• SequentialClaimsAdjudicationSystem: Complete adjudication workflow")
    print("• ClaimsFraudAnalyzer: Specialized fraud detection capabilities")
    print("• ClaimsWorkflowResult: Structured workflow execution results")
    
    print("\n💡 Getting Started Tips:")
    print("• Use SequentialClaimsAdjudicationSystem for complete claims processing")
    print("• Start with FNOL data processing and validation")
    print("• Use ClaimsFraudAnalyzer for specialized fraud detection")
    print("• Sequential workflows work best for regulated insurance processes")
    print("• Monitor workflow performance and stage completion times")
    print("• Implement proper error handling and rollback mechanisms")
    print("• Consider compliance and audit requirements in workflow design")
    
    return demo_results


if __name__ == "__main__":
    main()