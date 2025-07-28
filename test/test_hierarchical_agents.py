#!/usr/bin/env python3
"""
Hierarchical Multi-Agent System Testing for Loan Underwriting

This script provides comprehensive testing for the hierarchical loan underwriting system
using the HierarchicalLoanUnderwritingSystem class. It demonstrates how to test
hierarchical agent coordination, document processing, and loan decision making.

Usage:
    python test/test_hierarchical_agents.py

Requirements:
    - Run from the FSI-MAS root directory
    - Ensure .env file contains required AWS credentials for Bedrock
    - Dependencies must be installed in the graph_IntelligentLoanUnderwriting directory
"""

import sys
import os
import time
from pathlib import Path

# Add the graph_IntelligentLoanUnderwriting to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'graph_IntelligentLoanUnderwriting'))

try:
    from IntelligentLoanApplication_Graph import (
        HierarchicalLoanUnderwritingSystem,
        LoanDocumentProcessor,
        FraudDetectionAnalyzer,
        demonstrate_loan_underwriting_system,
        demonstrate_fraud_detection,
        explain_multi_agent_principles
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("⚠️  Running in demo mode - some functionality may be limited")
    DEPENDENCIES_AVAILABLE = False


def test_document_processing():
    """
    Test PDF document processing capabilities.
    
    Returns:
        Dictionary with test results
    """
    print("📄 TESTING DOCUMENT PROCESSING")
    print("-" * 50)
    
    # Initialize document processor
    processor = LoanDocumentProcessor()
    
    # Define sample documents path
    data_dir = Path(__file__).parent.parent / "graph_IntelligentLoanUnderwriting" / "data"
    
    sample_documents = {
        "credit_report": data_dir / "JoeDoeCreditReport.pdf",
        "bank_statement": data_dir / "JoeDoeBankStatement.pdf", 
        "pay_stub": data_dir / "JoeDoePayStub.pdf",
        "tax_return": data_dir / "JoeDoeTaxes.pdf",
        "loan_application": data_dir / "JoeDoeLoanApplication.pdf",
        "property_info": data_dir / "JoeDoePropertyInfo.pdf",
        "id_verification": data_dir / "JoeDoeIDVerification.pdf"
    }
    
    results = {
        "documents_processed": 0,
        "successful_extractions": 0,
        "failed_extractions": 0,
        "document_details": {},
        "total_pages": 0
    }
    
    for doc_type, file_path in sample_documents.items():
        print(f"Processing {doc_type}: {file_path.name}")
        
        if file_path.exists():
            doc_result = processor.read_loan_pdf(str(file_path))
            results["documents_processed"] += 1
            
            if doc_result["status"] == "success":
                results["successful_extractions"] += 1
                results["total_pages"] += doc_result["pages"]
                results["document_details"][doc_type] = {
                    "pages": doc_result["pages"],
                    "chars": doc_result["total_chars"],
                    "document_type": doc_result["document_analysis"]["document_type"],
                    "importance": doc_result["document_analysis"]["estimated_importance"]
                }
                print(f"  ✅ Success: {doc_result['pages']} pages, {doc_result['total_chars']} chars")
            else:
                results["failed_extractions"] += 1
                print(f"  ❌ Failed: {doc_result['message']}")
        else:
            print(f"  ⚠️  File not found: {file_path}")
            results["failed_extractions"] += 1
    
    print(f"\n📊 Document Processing Summary:")
    print(f"  Documents Processed: {results['documents_processed']}")
    print(f"  Successful: {results['successful_extractions']}")
    print(f"  Failed: {results['failed_extractions']}")
    print(f"  Total Pages: {results['total_pages']}")
    
    return results


def test_fraud_detection():
    """
    Test fraud detection capabilities.
    
    Returns:
        Dictionary with fraud detection test results
    """
    print("🕵️  TESTING FRAUD DETECTION")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Dependencies not available - running simplified test")
        return {"status": "demo", "message": "Limited testing due to missing dependencies"}
    
    # Run fraud detection demonstration
    print("Running fraud detection analysis...")
    fraud_results = demonstrate_fraud_detection()
    
    print(f"✅ Fraud detection test completed")
    print(f"  Fraud Score: {fraud_results['fraud_score']}")
    print(f"  Risk Level: {fraud_results['risk_level']}")
    print(f"  Indicators: {len(fraud_results['detected_indicators'])}")
    
    return fraud_results


def test_hierarchical_system_creation():
    """
    Test hierarchical agent system creation and setup.
    
    Returns:
        Dictionary with system creation test results
    """
    print("🏗️  TESTING HIERARCHICAL SYSTEM CREATION")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Dependencies not available - testing in demo mode")
    
    try:
        # Create hierarchical loan underwriting system
        print("Creating hierarchical loan underwriting system...")
        system = HierarchicalLoanUnderwritingSystem("test_loan_system")
        
        # Check system status
        print("Checking system status...")
        status = system.get_system_status()
        
        print(f"✅ System creation successful")
        print(f"  System Status: {status}")
        
        return {
            "creation_successful": True,
            "system_status": status,
            "system_id": "test_loan_system"
        }
        
    except Exception as e:
        print(f"❌ System creation failed: {str(e)}")
        return {
            "creation_successful": False,
            "error": str(e)
        }


def test_loan_processing():
    """
    Test complete loan application processing through hierarchical agents.
    
    Returns:
        Dictionary with loan processing test results
    """
    print("🏦 TESTING LOAN APPLICATION PROCESSING")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_loan_underwriting_system()
        return demo_results
    
    try:
        # Create system
        system = HierarchicalLoanUnderwritingSystem("loan_processing_test")
        
        # Define document paths
        data_dir = Path(__file__).parent.parent / "graph_IntelligentLoanUnderwriting" / "data"
        
        sample_documents = {
            "credit_report": str(data_dir / "JoeDoeCreditReport.pdf"),
            "bank_statement": str(data_dir / "JoeDoeBankStatement.pdf"),
            "pay_stub": str(data_dir / "JoeDoePayStub.pdf"),
            "tax_return": str(data_dir / "JoeDoeTaxes.pdf"),
            "loan_application": str(data_dir / "JoeDoeLoanApplication.pdf"),
            "property_info": str(data_dir / "JoeDoePropertyInfo.pdf"),
            "id_verification": str(data_dir / "JoeDoeIDVerification.pdf")
        }
        
        # Process loan application
        print("Processing loan application for Joe Doe...")
        loan_decision = system.process_loan_application(
            applicant_name="Joe Doe",
            document_paths=sample_documents,
            application_id="TEST_LOAN_001"
        )
        
        print(f"✅ Loan processing completed!")
        print(f"  Decision: {loan_decision.decision}")
        print(f"  Confidence: {loan_decision.confidence_score:.2f}")
        print(f"  Fraud Indicators: {len(loan_decision.fraud_indicators)}")
        print(f"  Recommendations: {len(loan_decision.recommendations)}")
        print(f"  Processing Time: {loan_decision.decision_timestamp}")
        
        # Shutdown system
        system.shutdown_system()
        
        return {
            "processing_successful": True,
            "decision": loan_decision.decision,
            "confidence_score": loan_decision.confidence_score,
            "fraud_indicators_count": len(loan_decision.fraud_indicators),
            "recommendations_count": len(loan_decision.recommendations),
            "processing_timestamp": loan_decision.decision_timestamp.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Loan processing failed: {str(e)}")
        return {
            "processing_successful": False,
            "error": str(e)
        }


def test_agent_hierarchy_communication():
    """
    Test communication patterns within the hierarchical agent structure.
    
    Returns:
        Dictionary with communication test results
    """
    print("📡 TESTING HIERARCHICAL AGENT COMMUNICATION")
    print("-" * 50)
    
    # Test agent role definitions and hierarchy
    from IntelligentLoanApplication_Graph import LoanUnderwritingConcepts
    
    concepts = LoanUnderwritingConcepts()
    agent_specs = concepts.agent_specializations()
    
    print("Validating agent hierarchy structure:")
    
    expected_agents = [
        "supervisor_agent",
        "financial_analysis_manager", 
        "risk_analysis_manager",
        "specialist_agents"
    ]
    
    communication_results = {
        "hierarchy_valid": True,
        "agent_roles_defined": {},
        "communication_patterns": {}
    }
    
    for agent_type in expected_agents:
        if agent_type in agent_specs:
            communication_results["agent_roles_defined"][agent_type] = True
            print(f"  ✅ {agent_type}: Defined")
            
            # Check role definitions
            if isinstance(agent_specs[agent_type], dict) and "role" in agent_specs[agent_type]:
                role = agent_specs[agent_type]["role"]
                print(f"     Role: {role}")
        else:
            communication_results["agent_roles_defined"][agent_type] = False
            communication_results["hierarchy_valid"] = False
            print(f"  ❌ {agent_type}: Missing")
    
    # Test hierarchy principles
    print("\nValidating hierarchical communication principles:")
    principles = explain_multi_agent_principles()
    
    if "use_case_guidance" in principles:
        guidance = principles["use_case_guidance"]
        print("  ✅ Use case guidance available")
        
        if "when_to_use_hierarchical" in guidance:
            print(f"     Hierarchical use cases: {len(guidance['when_to_use_hierarchical'])}")
        
        if "benefits_for_loan_underwriting" in guidance:
            print(f"     Loan underwriting benefits: {len(guidance['benefits_for_loan_underwriting'])}")
    
    return communication_results


def run_comprehensive_hierarchical_test():
    """
    Run comprehensive test suite for hierarchical multi-agent system.
    
    Returns:
        Dictionary with complete test results
    """
    print("🎯 COMPREHENSIVE HIERARCHICAL AGENT TESTING")
    print("=" * 70)
    
    test_results = {
        "start_time": time.time(),
        "tests_completed": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "results": {}
    }
    
    # Test 1: Document Processing
    try:
        print(f"\n{'='*70}")
        print("TEST 1: DOCUMENT PROCESSING")
        test_results["results"]["document_processing"] = test_document_processing()
        test_results["tests_completed"] += 1
        if test_results["results"]["document_processing"]["successful_extractions"] > 0:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Document processing test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["document_processing"] = {"error": str(e)}
    
    # Test 2: Fraud Detection
    try:
        print(f"\n{'='*70}")
        print("TEST 2: FRAUD DETECTION")
        test_results["results"]["fraud_detection"] = test_fraud_detection()
        test_results["tests_completed"] += 1
        test_results["tests_passed"] += 1
    except Exception as e:
        print(f"❌ Fraud detection test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["fraud_detection"] = {"error": str(e)}
    
    # Test 3: System Creation
    try:
        print(f"\n{'='*70}")
        print("TEST 3: SYSTEM CREATION")
        test_results["results"]["system_creation"] = test_hierarchical_system_creation()
        test_results["tests_completed"] += 1
        if test_results["results"]["system_creation"]["creation_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ System creation test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["system_creation"] = {"error": str(e)}
    
    # Test 4: Agent Communication
    try:
        print(f"\n{'='*70}")
        print("TEST 4: AGENT COMMUNICATION")
        test_results["results"]["agent_communication"] = test_agent_hierarchy_communication()
        test_results["tests_completed"] += 1
        if test_results["results"]["agent_communication"]["hierarchy_valid"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Agent communication test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["agent_communication"] = {"error": str(e)}
    
    # Test 5: Loan Processing (Most comprehensive)
    try:
        print(f"\n{'='*70}")
        print("TEST 5: LOAN PROCESSING")
        test_results["results"]["loan_processing"] = test_loan_processing()
        test_results["tests_completed"] += 1
        if test_results["results"]["loan_processing"].get("processing_successful", False):
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Loan processing test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["loan_processing"] = {"error": str(e)}
    
    # Calculate final results
    test_results["end_time"] = time.time()
    test_results["total_duration"] = test_results["end_time"] - test_results["start_time"]
    test_results["success_rate"] = test_results["tests_passed"] / test_results["tests_completed"] if test_results["tests_completed"] > 0 else 0
    
    # Print final summary
    print(f"\n{'='*70}")
    print("🏁 HIERARCHICAL AGENT TESTING COMPLETE")
    print(f"📊 Tests Completed: {test_results['tests_completed']}")
    print(f"✅ Tests Passed: {test_results['tests_passed']}")
    print(f"❌ Tests Failed: {test_results['tests_failed']}")
    print(f"📈 Success Rate: {test_results['success_rate']:.1%}")
    print(f"⏱️  Total Duration: {test_results['total_duration']:.2f} seconds")
    
    if test_results["success_rate"] >= 0.8:
        print("🎉 HIERARCHICAL SYSTEM TESTING: EXCELLENT")
    elif test_results["success_rate"] >= 0.6:
        print("👍 HIERARCHICAL SYSTEM TESTING: GOOD")
    else:
        print("⚠️  HIERARCHICAL SYSTEM TESTING: NEEDS IMPROVEMENT")
    
    return test_results


def main():
    """
    Main function for hierarchical agent testing.
    """
    print(__doc__)
    
    print("\n🔧 Environment Check:")
    print(f"  Dependencies Available: {DEPENDENCIES_AVAILABLE}")
    print(f"  Python Version: {sys.version}")
    print(f"  Current Directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    expected_dirs = ["graph_IntelligentLoanUnderwriting", "Finance-assistant-swarm-agent", "test"]
    current_contents = os.listdir(".")
    
    missing_dirs = [d for d in expected_dirs if d not in current_contents]
    if missing_dirs:
        print(f"⚠️  Warning: Missing expected directories: {missing_dirs}")
        print("   Make sure you're running from the FSI-MAS root directory")
    
    # Run comprehensive testing
    results = run_comprehensive_hierarchical_test()
    
    # Save results to file
    import json
    results_file = Path(__file__).parent / "hierarchical_test_results.json"
    
    # Convert datetime objects to strings for JSON serialization
    json_results = json.loads(json.dumps(results, default=str))
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()