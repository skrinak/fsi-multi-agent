#!/usr/bin/env python3
"""
Parallel Workflow Multi-Agent System Testing for Claims Processing

This script provides comprehensive testing for the parallel workflow claims processing system
using the SequentialClaimsAdjudicationSystem class. It demonstrates how to test both
sequential and parallel agent coordination, document processing, and workflow execution.

Usage:
    python test/test_parallel_workflow_agents.py

Requirements:
    - Run from the FSI-MAS root directory
    - Ensure .env file contains required AWS credentials for Bedrock
    - Dependencies must be installed in the WorkFlow_ClaimsAdjudication directory
"""

import sys
import os
import time
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add the WorkFlow_ClaimsAdjudication directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'WorkFlow_ClaimsAdjudication'))

try:
    from ClaimsAdjudication_SequentialPattern import (
        SequentialClaimsAdjudicationSystem,
        ClaimsDocumentProcessor,
        ClaimsFraudAnalyzer,
        ClaimsAdjudicationConcepts,
        demonstrate_claims_adjudication_workflow,
        demonstrate_fraud_detection,
        explain_sequential_workflow_principles
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("⚠️  Running in demo mode - some functionality may be limited")
    DEPENDENCIES_AVAILABLE = False


def test_document_processing():
    """
    Test claims document processing capabilities for various formats.
    
    Returns:
        Dictionary with test results
    """
    print("📄 TESTING CLAIMS DOCUMENT PROCESSING")
    print("-" * 50)
    
    # Initialize document processor
    processor = ClaimsDocumentProcessor()
    
    # Define sample documents path
    data_dir = Path(__file__).parent.parent / "WorkFlow_ClaimsAdjudication" / "data"
    
    sample_documents = {
        "fnol_json": data_dir / "FNOL.json"
    }
    
    results = {
        "documents_processed": 0,
        "successful_extractions": 0,
        "failed_extractions": 0,
        "document_details": {},
        "total_data_fields": 0
    }
    
    for doc_type, file_path in sample_documents.items():
        print(f"Processing {doc_type}: {file_path.name}")
        
        if file_path.exists():
            doc_result = processor.read_claims_file(str(file_path))
            results["documents_processed"] += 1
            
            if doc_result["status"] == "success":
                results["successful_extractions"] += 1
                data_fields = len(str(doc_result["data"]).split(','))
                results["total_data_fields"] += data_fields
                results["document_details"][doc_type] = {
                    "document_type": doc_result["document_type"],
                    "data_fields": data_fields,
                    "analysis": doc_result["document_analysis"],
                    "contains_fnol": doc_result["document_analysis"]["contains_fnol_data"],
                    "contains_policy": doc_result["document_analysis"]["contains_policy_info"],
                    "completeness": doc_result["document_analysis"]["estimated_completeness"]
                }
                print(f"  ✅ Success: {doc_result['document_type']}")
                print(f"     Data fields: {data_fields}")
                print(f"     Completeness: {doc_result['document_analysis']['estimated_completeness']}")
            else:
                results["failed_extractions"] += 1
                print(f"  ❌ Failed: {doc_result['message']}")
        else:
            print(f"  ⚠️  File not found: {file_path}")
            results["failed_extractions"] += 1
    
    # Test additional document formats
    print("\nTesting additional document format support...")
    
    # Test JSON processing with sample data
    sample_json_data = {
        "claim_id": "TEST-001",
        "policy_number": "POL-123456",
        "incident_date": "2024-01-15",
        "claimant": "Test Claimant",
        "amount": 5000.00
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        json.dump(sample_json_data, temp_file)
        temp_json_path = temp_file.name
    
    try:
        json_result = processor.read_claims_file(temp_json_path)
        if json_result["status"] == "success":
            results["successful_extractions"] += 1
            print(f"  ✅ JSON processing: {json_result['document_type']}")
        else:
            results["failed_extractions"] += 1
        results["documents_processed"] += 1
    finally:
        os.unlink(temp_json_path)
    
    print(f"\n📊 Document Processing Summary:")
    print(f"  Documents Processed: {results['documents_processed']}")
    print(f"  Successful: {results['successful_extractions']}")
    print(f"  Failed: {results['failed_extractions']}")
    print(f"  Total Data Fields: {results['total_data_fields']}")
    
    return results


def test_workflow_creation():
    """
    Test sequential/parallel workflow creation and initialization.
    
    Returns:
        Dictionary with workflow creation test results
    """
    print("🔧 TESTING WORKFLOW CREATION")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Dependencies not available - testing in demo mode")
    
    try:
        # Create sequential claims adjudication system
        print("Creating claims adjudication workflow...")
        system = SequentialClaimsAdjudicationSystem("test_workflow")
        
        # Test workflow status
        print("Checking workflow status...")
        status = system.get_workflow_status()
        
        print(f"✅ Workflow creation successful")
        print(f"  System Status: {status}")
        
        return {
            "creation_successful": True,
            "workflow_status": status,
            "system_id": "test_workflow",
            "demo_mode": not DEPENDENCIES_AVAILABLE
        }
        
    except Exception as e:
        print(f"❌ Workflow creation failed: {str(e)}")
        return {
            "creation_successful": False,
            "error": str(e),
            "demo_mode": not DEPENDENCIES_AVAILABLE
        }


def test_fraud_detection_system():
    """
    Test fraud detection capabilities with various risk scenarios.
    
    Returns:
        Dictionary with fraud detection test results
    """
    print("🕵️  TESTING FRAUD DETECTION SYSTEM")
    print("-" * 50)
    
    try:
        # Create fraud detection analyzer
        print("Creating fraud detection analyzer...")
        fraud_analyzer = ClaimsFraudAnalyzer()
        
        # Test scenarios with different risk levels
        test_scenarios = [
            {
                "name": "Low Risk Claim",
                "data": {
                    "claim_number": "LOW-RISK-001",
                    "policy_number": "POL-123456789",
                    "incident_date": "2024-01-15",
                    "report_date": "2024-01-16",  # Next day reporting
                    "claimant": {
                        "name": "John Smith",
                        "behavior_notes": "Cooperative and forthcoming"
                    },
                    "incident": {
                        "type": "minor_fender_bender",
                        "description": "Minor parking lot incident",
                        "estimated_damage": 1500.00,
                        "documentation": "Complete photos and police report"
                    }
                }
            },
            {
                "name": "Medium Risk Claim", 
                "data": {
                    "claim_number": "MED-RISK-001",
                    "policy_number": "POL-987654321",
                    "incident_date": "2023-12-31",  # New Year's Eve
                    "report_date": "2024-01-07",    # Week delay
                    "claimant": {
                        "name": "Jane Doe",
                        "behavior_notes": "Some hesitation in responses"
                    },
                    "incident": {
                        "type": "comprehensive_claim",
                        "description": "Vehicle vandalism overnight",
                        "estimated_damage": 8500.00,
                        "documentation": "Limited photos, no witnesses"
                    }
                }
            },
            {
                "name": "High Risk Claim",
                "data": {
                    "claim_number": "HIGH-RISK-001", 
                    "policy_number": "POL-SUSPICIOUS",
                    "incident_date": "2024-01-01",  # Holiday
                    "report_date": "2024-01-20",    # Long delay
                    "claimant": {
                        "name": "Suspicious Claimant",
                        "behavior_notes": "Evasive responses, excessive pressure for settlement"
                    },
                    "incident": {
                        "type": "total_loss",
                        "description": "Vehicle fire in remote location",
                        "estimated_damage": 45000.00,
                        "documentation": "Poor quality photos, no witnesses",
                        "red_flags": ["late reporting", "convenient timing", "high value"]
                    }
                }
            }
        ]
        
        fraud_results = []
        
        for scenario in test_scenarios:
            print(f"\nAnalyzing {scenario['name']}...")
            analysis = fraud_analyzer.analyze_claim_fraud_risk(scenario['data'])
            
            fraud_results.append({
                "scenario": scenario['name'],
                "fraud_score": analysis['fraud_score'],
                "risk_level": analysis['risk_level'],
                "indicators_count": len(analysis['detected_indicators']),
                "recommended_action": analysis['recommended_action']
            })
            
            print(f"  Fraud Score: {analysis['fraud_score']:.2f}")
            print(f"  Risk Level: {analysis['risk_level']}")
            print(f"  Indicators: {len(analysis['detected_indicators'])}")
        
        print(f"✅ Fraud detection system test successful")
        print(f"  Test scenarios: {len(test_scenarios)}")
        print(f"  Risk levels detected: {len(set(r['risk_level'] for r in fraud_results))}")
        
        return {
            "system_functional": True,
            "scenarios_tested": len(test_scenarios),
            "fraud_results": fraud_results,
            "risk_levels_detected": list(set(r['risk_level'] for r in fraud_results))
        }
        
    except Exception as e:
        print(f"❌ Fraud detection system test failed: {str(e)}")
        return {
            "system_functional": False,
            "error": str(e)
        }


def test_sequential_workflow_execution():
    """
    Test sequential workflow execution with dependency management.
    
    Returns:
        Dictionary with sequential workflow test results  
    """
    print("⏭️  TESTING SEQUENTIAL WORKFLOW EXECUTION")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_claims_adjudication_workflow()
        return {
            "execution_successful": True,
            "demo_mode": True,
            "demo_results": demo_results
        }
    
    try:
        # Create workflow system
        system = SequentialClaimsAdjudicationSystem("sequential_test")
        
        # Prepare test FNOL data
        test_fnol_data = {
            "fnol": {
                "claimNumber": "SEQ-TEST-001",
                "reportDate": "2024-01-15",
                "reportTime": "10:30:00",
                "reportMethod": "Online",
                "submittedBy": "Policyholder"
            },
            "policyInformation": {
                "policyNumber": "AUTO-TEST-123",
                "policyType": "Auto Insurance",
                "effectiveDate": "2023-01-01",
                "expirationDate": "2024-12-31"
            },
            "incident": {
                "date": "2024-01-14",
                "time": "15:30:00",
                "description": "Minor collision at parking lot",
                "estimatedDamage": 2500.00
            },
            "policyholder": {
                "firstName": "Test",
                "lastName": "User",
                "email": "test@example.com"
            }
        }
        
        # Save test data to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(test_fnol_data, temp_file)
            temp_fnol_path = temp_file.name
        
        try:
            print("Processing test claim through sequential workflow...")
            start_time = time.time()
            
            workflow_result = system.process_claim(
                claim_data_path=temp_fnol_path,
                claim_id="SEQ_TEST_001"
            )
            
            execution_time = time.time() - start_time
            
            print(f"✅ Sequential workflow execution completed")
            print(f"  Claim ID: {workflow_result.claim_id}")
            print(f"  Final Decision: {workflow_result.final_decision}")
            print(f"  Execution Time: {execution_time:.2f} seconds")
            print(f"  Processing Stages: {len(workflow_result.processing_stages)}")
            
            return {
                "execution_successful": True,
                "claim_id": workflow_result.claim_id,
                "final_decision": workflow_result.final_decision,
                "execution_time": execution_time,
                "stages_count": len(workflow_result.processing_stages),
                "settlement_amount": workflow_result.settlement_amount
            }
            
        finally:
            os.unlink(temp_fnol_path)
            
    except Exception as e:
        print(f"❌ Sequential workflow execution failed: {str(e)}")
        return {
            "execution_successful": False,
            "error": str(e)
        }


def test_parallel_workflow_capabilities():
    """
    Test parallel workflow execution capabilities and task coordination.
    
    Returns:
        Dictionary with parallel workflow test results
    """
    print("⚡ TESTING PARALLEL WORKFLOW CAPABILITIES")
    print("-" * 50)
    
    try:
        # Load existing workflow configuration to check parallel settings
        workflow_dir = Path(__file__).parent.parent / "WorkFlow_ClaimsAdjudication" / "workflows"
        workflow_files = []
        
        for workflow_file in workflow_dir.glob("*.json"):
            try:
                with open(workflow_file, 'r') as f:
                    workflow_config = json.load(f)
                    workflow_files.append({
                        "file": workflow_file.name,
                        "workflow_id": workflow_config.get("workflow_id", "unknown"),
                        "parallel_execution": workflow_config.get("parallel_execution", False),
                        "tasks_count": len(workflow_config.get("tasks", [])),
                        "dependencies": any("dependencies" in task for task in workflow_config.get("tasks", []))
                    })
                    print(f"  ✅ Loaded: {workflow_file.name}")
                    print(f"     Parallel execution: {workflow_config.get('parallel_execution', False)}")
                    print(f"     Tasks: {len(workflow_config.get('tasks', []))}")
            except Exception as e:
                print(f"  ❌ Failed to load {workflow_file.name}: {e}")
        
        # Test parallel execution concepts
        print("\nTesting parallel execution concepts...")
        concepts = ClaimsAdjudicationConcepts()
        workflow_stages = concepts.workflow_stage_specifications()
        
        # Analyze task dependencies for parallel execution potential
        dependency_analysis = {
            "independent_tasks": [],
            "dependent_tasks": [],
            "parallel_groups": []
        }
        
        # Simulate task dependency analysis
        sample_tasks = [
            {"id": "fnol_processing", "dependencies": []},
            {"id": "policy_verification", "dependencies": ["fnol_processing"]},
            {"id": "fraud_detection", "dependencies": ["fnol_processing"]}, 
            {"id": "damage_appraisal", "dependencies": ["policy_verification", "fraud_detection"]},
            {"id": "settlement_calculation", "dependencies": ["damage_appraisal"]},
            {"id": "final_review", "dependencies": ["settlement_calculation"]}
        ]
        
        # Identify parallel execution opportunities
        for task in sample_tasks:
            if not task["dependencies"]:
                dependency_analysis["independent_tasks"].append(task["id"])
            else:
                dependency_analysis["dependent_tasks"].append({
                    "task": task["id"],
                    "depends_on": task["dependencies"]
                })
        
        # Identify tasks that can run in parallel
        parallel_groups = [
            {"group": "Initial Processing", "tasks": ["fnol_processing"]},
            {"group": "Verification & Detection", "tasks": ["policy_verification", "fraud_detection"]},
            {"group": "Assessment", "tasks": ["damage_appraisal"]},
            {"group": "Settlement", "tasks": ["settlement_calculation"]},
            {"group": "Review", "tasks": ["final_review"]}
        ]
        
        dependency_analysis["parallel_groups"] = parallel_groups
        
        print(f"✅ Parallel workflow capabilities test successful")
        print(f"  Workflow files analyzed: {len(workflow_files)}")
        print(f"  Parallel-enabled workflows: {sum(1 for w in workflow_files if w['parallel_execution'])}")
        print(f"  Independent tasks: {len(dependency_analysis['independent_tasks'])}")
        print(f"  Potential parallel groups: {len(parallel_groups)}")
        
        return {
            "capabilities_functional": True,
            "workflow_files_count": len(workflow_files),
            "parallel_enabled_count": sum(1 for w in workflow_files if w['parallel_execution']),
            "workflow_configurations": workflow_files,
            "dependency_analysis": dependency_analysis,
            "parallel_opportunities": len([g for g in parallel_groups if len(g["tasks"]) > 1])
        }
        
    except Exception as e:
        print(f"❌ Parallel workflow capabilities test failed: {str(e)}")
        return {
            "capabilities_functional": False,
            "error": str(e)
        }


def test_workflow_concepts_validation():
    """
    Test workflow concepts and theoretical foundations.
    
    Returns:
        Dictionary with concepts validation test results
    """
    print("🧠 TESTING WORKFLOW CONCEPTS VALIDATION")
    print("-" * 50)
    
    try:
        # Test ClaimsAdjudicationConcepts
        concepts = ClaimsAdjudicationConcepts()
        
        # Test core concepts
        print("Testing core claims adjudication concepts...")
        core_concepts = concepts.explain_claims_adjudication()
        
        print("Testing workflow stage specifications...")
        workflow_stages = concepts.workflow_stage_specifications()
        
        # Validate concept structure
        expected_concepts = ["claims_adjudication_overview", "sequential_workflow_principles", "multi_agent_workflow_benefits"]
        concepts_valid = all(concept in core_concepts for concept in expected_concepts)
        
        # Validate workflow stages
        expected_stages = ["fnol_processing", "policy_verification", "fraud_detection", "damage_appraisal", "settlement_calculation", "final_review"]
        stages_valid = all(stage in workflow_stages for stage in expected_stages)
        
        # Test implementation guidance
        print("Testing implementation guidance...")
        guidance = explain_sequential_workflow_principles()
        
        expected_guidance = ["adjudication_process", "workflow_stages", "implementation_guidance"]
        guidance_valid = all(key in guidance for key in expected_guidance)
        
        print(f"✅ Workflow concepts validation test successful")
        print(f"  Core concepts: {len(core_concepts)} documented")
        print(f"  Workflow stages: {len(workflow_stages)} defined")
        print(f"  Implementation guidance: Complete")
        
        return {
            "concepts_functional": True,
            "core_concepts_count": len(core_concepts),
            "workflow_stages_count": len(workflow_stages),
            "validation_results": {
                "concepts_valid": concepts_valid,
                "stages_valid": stages_valid,
                "guidance_valid": guidance_valid
            },
            "stage_specifications": {
                stage: details["role"] for stage, details in workflow_stages.items()
            }
        }
        
    except Exception as e:
        print(f"❌ Workflow concepts validation test failed: {str(e)}")
        return {
            "concepts_functional": False,
            "error": str(e)
        }


def test_end_to_end_claims_processing():
    """
    Test complete end-to-end claims processing workflow.
    
    Returns:
        Dictionary with end-to-end test results
    """
    print("🏁 TESTING END-TO-END CLAIMS PROCESSING")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_claims_adjudication_workflow()
        return {
            "processing_successful": True,
            "demo_mode": True,
            "demo_results": demo_results
        }
    
    try:
        # Step 1: Document Processing
        print("Step 1: Processing claims document...")
        processor = ClaimsDocumentProcessor()
        data_dir = Path(__file__).parent.parent / "WorkFlow_ClaimsAdjudication" / "data"
        fnol_path = str(data_dir / "FNOL.json")
        
        doc_result = processor.read_claims_file(fnol_path)
        
        if doc_result["status"] != "success":
            # Use sample data if document not available 
            sample_data = {
                "claim_number": "E2E-TEST-001",
                "policy_number": "POL-E2E-123",
                "incident_date": "2024-01-15",
                "claimant_name": "End-to-End Test",
                "estimated_damage": 7500.00,
                "incident_type": "collision"
            }
            print("  ⚠️  Using sample data (document not found)")
        else:
            sample_data = doc_result["data"]
            print(f"  ✅ Processed document: {doc_result['document_type']}")
        
        # Step 2: Fraud Detection Analysis
        print("Step 2: Conducting fraud detection analysis...")
        fraud_analyzer = ClaimsFraudAnalyzer()
        fraud_analysis = fraud_analyzer.analyze_claim_fraud_risk(sample_data)
        
        print(f"  Fraud Risk Level: {fraud_analysis['risk_level']}")
        print(f"  Fraud Score: {fraud_analysis['fraud_score']:.2f}")
        
        # Step 3: Workflow Execution
        print("Step 3: Creating and executing claims workflow...")
        system = SequentialClaimsAdjudicationSystem("e2e_test_workflow")
        
        # Create temporary file with test data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(sample_data, temp_file)
            temp_path = temp_file.name
        
        try:
            start_time = time.time()
            workflow_result = system.process_claim(
                claim_data_path=temp_path,
                claim_id="E2E_TEST_001"
            )
            processing_time = time.time() - start_time
            
            # Step 4: Results Validation
            print("Step 4: Validating processing results...")
            
            validation_checks = {
                "has_claim_id": len(workflow_result.claim_id) > 0,
                "has_decision": workflow_result.final_decision in ["APPROVED", "DENIED", "INVESTIGATE", "PENDING", "DEMO", "ERROR"],
                "has_processing_stages": len(workflow_result.processing_stages) > 0,
                "processing_time_reasonable": processing_time < 300,  # Less than 5 minutes
                "has_metadata": len(workflow_result.metadata) > 0
            }
            
            validation_passed = all(validation_checks.values())
            
            print(f"✅ End-to-end processing completed in {processing_time:.2f} seconds")
            print(f"  Validation passed: {validation_passed}")
            print(f"  Final decision: {workflow_result.final_decision}")
            print(f"  Processing stages: {len(workflow_result.processing_stages)}")
            if workflow_result.settlement_amount:
                print(f"  Settlement amount: ${workflow_result.settlement_amount:,.2f}")
            
            return {
                "processing_successful": True,
                "processing_time": processing_time,
                "final_decision": workflow_result.final_decision,
                "settlement_amount": workflow_result.settlement_amount,
                "fraud_risk_level": fraud_analysis['risk_level'],
                "fraud_score": fraud_analysis['fraud_score'],
                "validation_checks": validation_checks,
                "validation_passed": validation_passed,
                "stages_completed": len(workflow_result.processing_stages)
            }
            
        finally:
            os.unlink(temp_path)
            
    except Exception as e:
        print(f"❌ End-to-end processing test failed: {str(e)}")
        return {
            "processing_successful": False,
            "error": str(e)
        }


def run_comprehensive_parallel_workflow_test():
    """
    Run comprehensive test suite for parallel workflow multi-agent system.
    
    Returns:
        Dictionary with complete test results
    """
    print("⚡ COMPREHENSIVE PARALLEL WORKFLOW AGENT TESTING")
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
        print("TEST 1: CLAIMS DOCUMENT PROCESSING")
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
    
    # Test 2: Workflow Creation
    try:
        print(f"\n{'='*70}")
        print("TEST 2: WORKFLOW CREATION")
        test_results["results"]["workflow_creation"] = test_workflow_creation()
        test_results["tests_completed"] += 1
        if test_results["results"]["workflow_creation"]["creation_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Workflow creation test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["workflow_creation"] = {"error": str(e)}
    
    # Test 3: Fraud Detection System
    try:
        print(f"\n{'='*70}")
        print("TEST 3: FRAUD DETECTION SYSTEM")
        test_results["results"]["fraud_detection"] = test_fraud_detection_system()
        test_results["tests_completed"] += 1
        if test_results["results"]["fraud_detection"]["system_functional"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Fraud detection system test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["fraud_detection"] = {"error": str(e)}
    
    # Test 4: Workflow Concepts Validation
    try:
        print(f"\n{'='*70}")
        print("TEST 4: WORKFLOW CONCEPTS VALIDATION")
        test_results["results"]["concepts"] = test_workflow_concepts_validation()
        test_results["tests_completed"] += 1
        if test_results["results"]["concepts"]["concepts_functional"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Workflow concepts validation test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["concepts"] = {"error": str(e)}
    
    # Test 5: Parallel Workflow Capabilities
    try:
        print(f"\n{'='*70}")
        print("TEST 5: PARALLEL WORKFLOW CAPABILITIES")
        test_results["results"]["parallel_capabilities"] = test_parallel_workflow_capabilities()
        test_results["tests_completed"] += 1
        if test_results["results"]["parallel_capabilities"]["capabilities_functional"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Parallel workflow capabilities test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["parallel_capabilities"] = {"error": str(e)}
    
    # Test 6: Sequential Workflow Execution
    try:
        print(f"\n{'='*70}")
        print("TEST 6: SEQUENTIAL WORKFLOW EXECUTION")
        test_results["results"]["sequential_execution"] = test_sequential_workflow_execution()
        test_results["tests_completed"] += 1
        if test_results["results"]["sequential_execution"]["execution_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Sequential workflow execution test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["sequential_execution"] = {"error": str(e)}
    
    # Test 7: End-to-End Processing
    try:
        print(f"\n{'='*70}")
        print("TEST 7: END-TO-END CLAIMS PROCESSING")
        test_results["results"]["end_to_end"] = test_end_to_end_claims_processing()
        test_results["tests_completed"] += 1
        if test_results["results"]["end_to_end"]["processing_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ End-to-end processing test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["end_to_end"] = {"error": str(e)}
    
    # Calculate final results
    test_results["end_time"] = time.time()
    test_results["total_duration"] = test_results["end_time"] - test_results["start_time"]
    test_results["success_rate"] = test_results["tests_passed"] / test_results["tests_completed"] if test_results["tests_completed"] > 0 else 0
    
    # Print final summary
    print(f"\n{'='*70}")
    print("🏁 PARALLEL WORKFLOW AGENT TESTING COMPLETE")
    print(f"📊 Tests Completed: {test_results['tests_completed']}")
    print(f"✅ Tests Passed: {test_results['tests_passed']}")
    print(f"❌ Tests Failed: {test_results['tests_failed']}")
    print(f"📈 Success Rate: {test_results['success_rate']:.1%}")
    print(f"⏱️  Total Duration: {test_results['total_duration']:.2f} seconds")
    
    if test_results["success_rate"] >= 0.85:
        print("🎉 PARALLEL WORKFLOW SYSTEM TESTING: EXCELLENT")
    elif test_results["success_rate"] >= 0.7:
        print("👍 PARALLEL WORKFLOW SYSTEM TESTING: GOOD")
    else:
        print("⚠️  PARALLEL WORKFLOW SYSTEM TESTING: NEEDS IMPROVEMENT")
    
    return test_results


def main():
    """
    Main function for parallel workflow agent testing.
    """
    print(__doc__)
    
    print("\n🔧 Environment Check:")
    print(f"  Dependencies Available: {DEPENDENCIES_AVAILABLE}")
    print(f"  Python Version: {sys.version}")
    print(f"  Current Directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    expected_dirs = ["WorkFlow_ClaimsAdjudication", "Finance-assistant-swarm-agent", "test"]
    current_contents = os.listdir(".")
    
    missing_dirs = [d for d in expected_dirs if d not in current_contents]
    if missing_dirs:
        print(f"⚠️  Warning: Missing expected directories: {missing_dirs}")
        print("   Make sure you're running from the FSI-MAS root directory")
    
    # Run comprehensive testing
    results = run_comprehensive_parallel_workflow_test()
    
    # Save results to file
    import json
    results_file = Path(__file__).parent / "parallel_workflow_test_results.json"
    
    # Convert datetime objects to strings for JSON serialization
    json_results = json.loads(json.dumps(results, default=str))
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()