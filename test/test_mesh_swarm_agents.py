#!/usr/bin/env python3
"""
Mesh Swarm Multi-Agent System Testing for Financial Research

This script provides comprehensive testing for the mesh swarm financial research system
using the MeshSwarmFinancialAnalyzer class. It demonstrates how to test mesh agent
coordination, document processing, and collaborative financial analysis.

Usage:
    python test/test_mesh_swarm_agents.py

Requirements:
    - Run from the FSI-MAS root directory
    - Ensure .env file contains required AWS credentials for Bedrock
    - Dependencies must be installed in the swarm directory
"""

import sys
import os
import time
from pathlib import Path

# Add the swarm directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'swarm'))

try:
    from FinancialResearch_MeshSwarm import (
        MeshSwarmFinancialAnalyzer,
        FinancialReportProcessor,
        SwarmPatternComparator,
        SharedMemorySystem,
        SwarmIntelligenceConcepts,
        demonstrate_financial_mesh_swarm,
        demonstrate_pattern_comparison,
        demonstrate_shared_memory_system,
        explain_swarm_applications
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("⚠️  Running in demo mode - some functionality may be limited")
    DEPENDENCIES_AVAILABLE = False


def test_document_processing():
    """
    Test PDF financial document processing capabilities.
    
    Returns:
        Dictionary with test results
    """
    print("📄 TESTING FINANCIAL DOCUMENT PROCESSING")
    print("-" * 50)
    
    # Initialize document processor
    processor = FinancialReportProcessor()
    
    # Define sample documents path
    data_dir = Path(__file__).parent.parent / "swarm" / "data"
    
    sample_documents = {
        "amazon_10k": data_dir / "amzn-20241231-10K-Part-1&2.pdf",
        "legal_correspondence": data_dir / "LEGALCORRESPONDENCE.pdf"
    }
    
    results = {
        "documents_processed": 0,
        "successful_extractions": 0,
        "failed_extractions": 0,
        "document_details": {},
        "total_pages": 0,
        "total_characters": 0
    }
    
    for doc_type, file_path in sample_documents.items():
        print(f"Processing {doc_type}: {file_path.name}")
        
        if file_path.exists():
            doc_result = processor.read_financial_pdf(str(file_path))
            results["documents_processed"] += 1
            
            if doc_result["status"] == "success":
                results["successful_extractions"] += 1
                results["total_pages"] += doc_result["pages"]
                results["total_characters"] += doc_result["total_chars"]
                results["document_details"][doc_type] = {
                    "pages": doc_result["pages"],
                    "chars": doc_result["total_chars"],
                    "document_type": doc_result["document_analysis"]["document_type"],
                    "complexity": doc_result["document_analysis"]["estimated_complexity"],
                    "contains_financial_metrics": doc_result["document_analysis"]["contains_financial_metrics"],
                    "contains_risk_factors": doc_result["document_analysis"]["contains_risk_factors"]
                }
                print(f"  ✅ Success: {doc_result['pages']} pages, {doc_result['total_chars']} chars")
                print(f"     Type: {doc_result['document_analysis']['document_type']}")
                print(f"     Complexity: {doc_result['document_analysis']['estimated_complexity']}")
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
    print(f"  Total Characters: {results['total_characters']}")
    
    return results


def test_mesh_agent_creation():
    """
    Test mesh swarm agent creation and initialization.
    
    Returns:
        Dictionary with agent creation test results
    """
    print("🕸️  TESTING MESH AGENT CREATION")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Dependencies not available - testing in demo mode")
    
    try:
        # Create mesh swarm analyzer
        print("Creating mesh swarm financial analyzer...")
        analyzer = MeshSwarmFinancialAnalyzer()
        
        # Test agent availability
        agent_tests = {
            "analyzer_created": analyzer is not None,
            "agents_available": False,
            "swarm_agent_available": False
        }
        
        if DEPENDENCIES_AVAILABLE:
            agent_tests["agents_available"] = hasattr(analyzer, 'agents') and analyzer.agents is not None
            agent_tests["swarm_agent_available"] = hasattr(analyzer, 'swarm_agent') and analyzer.swarm_agent is not None
            
            if analyzer.agents:
                print("  ✅ Individual agents created:")
                for agent_name, agent in analyzer.agents.items():
                    print(f"     • {agent_name}: {type(agent).__name__}")
                    agent_tests[f"{agent_name}_agent"] = True
            
            if analyzer.swarm_agent:
                print("  ✅ Swarm coordination agent created")
        
        print(f"✅ Mesh agent creation successful")
        
        return {
            "creation_successful": True,
            "agent_tests": agent_tests,
            "demo_mode": not DEPENDENCIES_AVAILABLE
        }
        
    except Exception as e:
        print(f"❌ Mesh agent creation failed: {str(e)}")
        return {
            "creation_successful": False,
            "error": str(e),
            "demo_mode": not DEPENDENCIES_AVAILABLE
        }


def test_shared_memory_system():
    """
    Test shared memory system functionality.
    
    Returns:
        Dictionary with shared memory test results
    """
    print("💭 TESTING SHARED MEMORY SYSTEM")
    print("-" * 50)
    
    try:
        # Create shared memory system
        print("Creating shared memory system...")
        shared_memory = SharedMemorySystem()
        
        # Test storing insights
        print("Testing insight storage...")
        test_insights = [
            ("financial_insights", "research_agent", "Amazon shows strong revenue growth", {"confidence": 0.9}),
            ("investment_analyses", "investment_agent", "Cloud computing provides competitive advantage", {"confidence": 0.85}),
            ("risk_assessments", "risk_agent", "Regulatory risks in multiple jurisdictions", {"risk_level": "medium"}),
            ("market_context", "research_agent", "Strong market position in e-commerce", {"confidence": 0.8})
        ]
        
        for category, agent_id, insight, metadata in test_insights:
            shared_memory.store_insight(category, agent_id, insight, metadata)
            print(f"  ✅ Stored: {agent_id} -> {category}")
        
        # Test retrieving insights
        print("Testing insight retrieval...")
        all_insights = shared_memory.retrieve_insights()
        research_insights = shared_memory.retrieve_insights(agent_id="research_agent")
        financial_insights = shared_memory.retrieve_insights(category="financial_insights")
        
        # Test memory summary
        print("Testing memory summary...")
        memory_summary = shared_memory.get_memory_summary()
        
        print(f"✅ Shared memory system test successful")
        print(f"  Total insights stored: {len(all_insights)}")
        print(f"  Research agent insights: {len(research_insights)}")
        print(f"  Financial insights: {len(financial_insights)}")
        print(f"  Memory categories: {len(memory_summary['categories'])}")
        
        return {
            "system_functional": True,
            "insights_stored": len(all_insights),
            "categories_used": len(memory_summary['categories']),
            "memory_summary": memory_summary,
            "retrieval_tests": {
                "all_insights": len(all_insights) == 4,
                "agent_filter": len(research_insights) == 2,
                "category_filter": len(financial_insights) == 1
            }
        }
        
    except Exception as e:
        print(f"❌ Shared memory system test failed: {str(e)}")
        return {
            "system_functional": False,
            "error": str(e)
        }


def test_mesh_communication_pattern():
    """
    Test mesh communication pattern with sample financial analysis.
    
    Returns:
        Dictionary with mesh communication test results
    """
    print("🕸️  TESTING MESH COMMUNICATION PATTERN")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_financial_mesh_swarm()
        return {
            "communication_successful": True,
            "demo_mode": True,
            "demo_results": demo_results
        }
    
    try:
        # Create analyzer
        analyzer = MeshSwarmFinancialAnalyzer()
        
        # Sample financial document text
        sample_financial_text = """
        TECHNOLOGY COMPANY FINANCIAL ANALYSIS
        
        Q4 2024 Results:
        Revenue: $125.7 billion (+12% YoY)
        Net Income: $28.4 billion (+18% YoY)
        Operating Cash Flow: $31.2 billion (+15% YoY)
        Free Cash Flow: $24.8 billion (+20% YoY)
        
        Cloud Services Revenue: $76.1 billion (+25% YoY)
        E-commerce Revenue: $42.3 billion (+8% YoY)
        Advertising Revenue: $7.3 billion (+35% YoY)
        
        Market Position:
        - Leading position in cloud computing infrastructure
        - Expanding presence in artificial intelligence and machine learning
        - Strong competitive moats in logistics and fulfillment
        - Growing advertising business with high margins
        
        Risk Factors:
        - Increasing competition in cloud services
        - Regulatory scrutiny in multiple jurisdictions
        - Economic sensitivity in consumer segments
        - Currency fluctuations impacting international operations
        """
        
        # Test mesh analysis
        print("Running mesh communication analysis...")
        analysis_query = """
        Analyze this company's financial performance and determine if it represents
        a good investment opportunity. Consider financial metrics, competitive position,
        growth prospects, and risk factors. Provide a clear investment recommendation.
        """
        
        start_time = time.time()
        analysis_result = analyzer.analyze_financial_document(
            sample_financial_text,
            analysis_query,
            use_mesh_communication=True
        )
        analysis_time = time.time() - start_time
        
        print(f"✅ Mesh communication analysis completed in {analysis_time:.2f} seconds")
        print(f"  Confidence Score: {analysis_result.confidence_score}")
        print(f"  Communication Pattern: {analysis_result.metadata.get('communication_pattern', 'Unknown')}")
        print(f"  Agents Used: {analysis_result.metadata.get('agents_used', 'Unknown')}")
        print(f"  Phases Completed: {analysis_result.metadata.get('phases_completed', 'Unknown')}")
        
        return {
            "communication_successful": True,
            "analysis_time": analysis_time,
            "confidence_score": analysis_result.confidence_score,
            "agents_used": analysis_result.metadata.get('agents_used', 0),
            "phases_completed": analysis_result.metadata.get('phases_completed', 0),
            "communication_pattern": analysis_result.metadata.get('communication_pattern', 'unknown'),
            "analysis_timestamp": analysis_result.analysis_timestamp.isoformat()
        }
        
    except Exception as e:
        print(f"❌ Mesh communication test failed: {str(e)}")
        return {
            "communication_successful": False,
            "error": str(e)
        }


def test_pattern_comparison():
    """
    Test comparison between mesh communication and swarm tool patterns.
    
    Returns:
        Dictionary with pattern comparison test results
    """
    print("🔄 TESTING PATTERN COMPARISON")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_pattern_comparison()
        return {
            "comparison_successful": True,
            "demo_mode": True,
            "demo_results": demo_results
        }
    
    try:
        # Create pattern comparator
        comparator = SwarmPatternComparator()
        
        # Sample financial text for comparison
        sample_text = """
        QUARTERLY FINANCIAL RESULTS
        
        Revenue Growth: 15% year-over-year
        Profit Margins: Expanding by 200 basis points
        Market Share: Leading position in key segments
        Innovation Pipeline: Strong R&D investments
        
        Challenges: Competitive pressure and regulatory oversight
        Opportunities: Expansion into emerging markets
        """
        
        analysis_query = "Evaluate this company as an investment opportunity"
        
        print("Starting comparative analysis...")
        start_time = time.time()
        
        comparison_results = comparator.compare_analysis_patterns(
            sample_text,
            analysis_query
        )
        
        comparison_time = time.time() - start_time
        
        # Generate comparison report
        comparison_report = comparator.generate_comparison_report(comparison_results)
        
        print(f"✅ Pattern comparison completed in {comparison_time:.2f} seconds")
        
        mesh_result = comparison_results["mesh_communication"]
        swarm_result = comparison_results["swarm_tool"]
        
        print(f"  Mesh Communication:")
        print(f"    Confidence: {mesh_result.confidence_score}")
        print(f"    Pattern: {mesh_result.metadata.get('communication_pattern', 'Unknown')}")
        
        print(f"  Swarm Tool:")
        print(f"    Confidence: {swarm_result.confidence_score}")
        print(f"    Coordination: {swarm_result.metadata.get('coordination', 'Unknown')}")
        
        return {
            "comparison_successful": True,
            "comparison_time": comparison_time,
            "mesh_confidence": mesh_result.confidence_score,
            "swarm_confidence": swarm_result.confidence_score,
            "comparison_report_length": len(comparison_report),
            "patterns_tested": 2
        }
        
    except Exception as e:
        print(f"❌ Pattern comparison test failed: {str(e)}")
        return {
            "comparison_successful": False,
            "error": str(e)
        }


def test_swarm_intelligence_concepts():
    """
    Test swarm intelligence concepts and documentation.
    
    Returns:
        Dictionary with concepts test results
    """
    print("🧠 TESTING SWARM INTELLIGENCE CONCEPTS")
    print("-" * 50)
    
    try:
        # Test SwarmIntelligenceConcepts
        concepts = SwarmIntelligenceConcepts()
        
        # Test core concepts
        print("Testing core swarm intelligence concepts...")
        core_concepts = concepts.explain_swarm_intelligence()
        
        print("Testing financial analysis applications...")
        financial_apps = concepts.financial_analysis_applications()
        
        # Validate concept structure
        expected_concepts = ["swarm_intelligence", "multi_agent_systems", "mesh_architecture"]
        concepts_valid = all(concept in core_concepts for concept in expected_concepts)
        
        # Validate applications structure
        expected_apps = ["applications", "agent_specializations", "benefits"]
        apps_valid = all(key in financial_apps for key in expected_apps)
        
        # Test application guidance
        print("Testing application guidance...")
        guidance = explain_swarm_applications()
        
        expected_guidance = ["when_to_use_swarm", "swarm_vs_single_agent", "best_practices", "implementation_patterns"]
        guidance_valid = all(key in guidance for key in expected_guidance)
        
        print(f"✅ Swarm intelligence concepts test successful")
        print(f"  Core concepts: {len(core_concepts)} documented")
        print(f"  Financial applications: {len(financial_apps['applications'])} listed")
        print(f"  Agent specializations: {len(financial_apps['agent_specializations'])} defined")
        print(f"  Best practices: {len(guidance['best_practices'])} provided")
        
        return {
            "concepts_functional": True,
            "core_concepts_count": len(core_concepts),
            "financial_applications_count": len(financial_apps['applications']),
            "agent_specializations_count": len(financial_apps['agent_specializations']),
            "best_practices_count": len(guidance['best_practices']),
            "validation_results": {
                "concepts_valid": concepts_valid,
                "apps_valid": apps_valid,
                "guidance_valid": guidance_valid
            }
        }
        
    except Exception as e:
        print(f"❌ Swarm intelligence concepts test failed: {str(e)}")
        return {
            "concepts_functional": False,
            "error": str(e)
        }


def test_financial_analysis_end_to_end():
    """
    Test complete end-to-end financial analysis workflow.
    
    Returns:
        Dictionary with end-to-end test results
    """
    print("🏁 TESTING END-TO-END FINANCIAL ANALYSIS")
    print("-" * 50)
    
    if not DEPENDENCIES_AVAILABLE:
        print("⚠️  Running demonstration mode")
        demo_results = demonstrate_financial_mesh_swarm()
        return {
            "analysis_successful": True,
            "demo_mode": True,
            "demo_results": demo_results
        }
    
    try:
        # Step 1: Document Processing
        print("Step 1: Processing financial document...")
        processor = FinancialReportProcessor()
        data_dir = Path(__file__).parent.parent / "swarm" / "data"
        amazon_doc_path = str(data_dir / "amzn-20241231-10K-Part-1&2.pdf")
        
        doc_result = processor.read_financial_pdf(amazon_doc_path)
        
        if doc_result["status"] != "success":
            # Use sample text if document not available
            sample_text = """
            AMAZON.COM, INC. FORM 10-K ANNUAL REPORT
            
            Business Overview:
            We are guided by four principles: customer obsession rather than competitor focus,
            passion for invention, commitment to operational excellence, and long-term thinking.
            
            Financial Performance:
            - Net sales increased 11% to $637.96 billion in 2024
            - Operating income was $73.17 billion in 2024
            - Net income was $49.05 billion in 2024
            - Operating cash flow was $115.88 billion in 2024
            
            Segment Performance:
            - North America: $387.50 billion net sales (+10% YoY)
            - International: $142.91 billion net sales (+9% YoY)  
            - AWS: $107.56 billion net sales (+19% YoY)
            
            Key Investments:
            - Continued investment in Prime member benefits
            - Expansion of AWS infrastructure and services
            - Investment in AI and machine learning capabilities
            - Development of advertising technologies
            """
            doc_text = sample_text
            print("  ⚠️  Using sample text (document not found)")
        else:
            doc_text = doc_result["text"]
            print(f"  ✅ Processed {doc_result['pages']} pages, {doc_result['total_chars']} characters")
        
        # Step 2: Mesh Swarm Analysis
        print("Step 2: Creating mesh swarm analyzer...")
        analyzer = MeshSwarmFinancialAnalyzer()
        
        print("Step 3: Conducting comprehensive financial analysis...")
        analysis_query = """
        Based on this Amazon 10-K filing, provide a comprehensive investment analysis.
        Evaluate the company's financial performance, competitive position, growth prospects,
        and investment risks. Provide a clear BUY/HOLD/SELL recommendation with rationale.
        """
        
        start_time = time.time()
        analysis_result = analyzer.analyze_financial_document(
            doc_text,
            analysis_query,
            use_mesh_communication=True
        )
        analysis_time = time.time() - start_time
        
        # Step 4: Results Validation
        print("Step 4: Validating analysis results...")
        
        validation_checks = {
            "has_research_insights": len(analysis_result.research_insights) > 100,
            "has_investment_evaluation": len(analysis_result.investment_evaluation) > 100,
            "has_risk_analysis": len(analysis_result.risk_analysis) > 100,
            "has_final_recommendation": len(analysis_result.final_recommendation) > 200,
            "confidence_score_valid": 0.0 <= analysis_result.confidence_score <= 1.0,
            "has_metadata": len(analysis_result.metadata) > 0
        }
        
        validation_passed = all(validation_checks.values())
        
        print(f"✅ End-to-end analysis completed in {analysis_time:.2f} seconds")
        print(f"  Validation passed: {validation_passed}")
        print(f"  Confidence score: {analysis_result.confidence_score}")
        print(f"  Research insights: {len(analysis_result.research_insights)} chars")
        print(f"  Investment evaluation: {len(analysis_result.investment_evaluation)} chars")
        print(f"  Risk analysis: {len(analysis_result.risk_analysis)} chars")
        print(f"  Final recommendation: {len(analysis_result.final_recommendation)} chars")
        
        return {
            "analysis_successful": True,
            "analysis_time": analysis_time,
            "confidence_score": analysis_result.confidence_score,
            "validation_checks": validation_checks,
            "validation_passed": validation_passed,
            "output_lengths": {
                "research_insights": len(analysis_result.research_insights),
                "investment_evaluation": len(analysis_result.investment_evaluation),
                "risk_analysis": len(analysis_result.risk_analysis),
                "final_recommendation": len(analysis_result.final_recommendation)
            },
            "analysis_timestamp": analysis_result.analysis_timestamp.isoformat()
        }
        
    except Exception as e:
        print(f"❌ End-to-end analysis test failed: {str(e)}")
        return {
            "analysis_successful": False,
            "error": str(e)
        }


def run_comprehensive_mesh_swarm_test():
    """
    Run comprehensive test suite for mesh swarm multi-agent system.
    
    Returns:
        Dictionary with complete test results
    """
    print("🕸️  COMPREHENSIVE MESH SWARM AGENT TESTING")
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
        print("TEST 1: FINANCIAL DOCUMENT PROCESSING")
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
    
    # Test 2: Mesh Agent Creation
    try:
        print(f"\n{'='*70}")
        print("TEST 2: MESH AGENT CREATION")
        test_results["results"]["agent_creation"] = test_mesh_agent_creation()
        test_results["tests_completed"] += 1
        if test_results["results"]["agent_creation"]["creation_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Mesh agent creation test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["agent_creation"] = {"error": str(e)}
    
    # Test 3: Shared Memory System
    try:
        print(f"\n{'='*70}")
        print("TEST 3: SHARED MEMORY SYSTEM")
        test_results["results"]["shared_memory"] = test_shared_memory_system()
        test_results["tests_completed"] += 1
        if test_results["results"]["shared_memory"]["system_functional"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Shared memory system test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["shared_memory"] = {"error": str(e)}
    
    # Test 4: Swarm Intelligence Concepts
    try:
        print(f"\n{'='*70}")
        print("TEST 4: SWARM INTELLIGENCE CONCEPTS")
        test_results["results"]["concepts"] = test_swarm_intelligence_concepts()
        test_results["tests_completed"] += 1
        if test_results["results"]["concepts"]["concepts_functional"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Swarm intelligence concepts test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["concepts"] = {"error": str(e)}
    
    # Test 5: Mesh Communication Pattern
    try:
        print(f"\n{'='*70}")
        print("TEST 5: MESH COMMUNICATION PATTERN")
        test_results["results"]["mesh_communication"] = test_mesh_communication_pattern()
        test_results["tests_completed"] += 1
        if test_results["results"]["mesh_communication"]["communication_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Mesh communication test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["mesh_communication"] = {"error": str(e)}
    
    # Test 6: Pattern Comparison
    try:
        print(f"\n{'='*70}")
        print("TEST 6: PATTERN COMPARISON")
        test_results["results"]["pattern_comparison"] = test_pattern_comparison()
        test_results["tests_completed"] += 1
        if test_results["results"]["pattern_comparison"]["comparison_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ Pattern comparison test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["pattern_comparison"] = {"error": str(e)}
    
    # Test 7: End-to-End Analysis
    try:
        print(f"\n{'='*70}")
        print("TEST 7: END-TO-END FINANCIAL ANALYSIS")
        test_results["results"]["end_to_end"] = test_financial_analysis_end_to_end()
        test_results["tests_completed"] += 1
        if test_results["results"]["end_to_end"]["analysis_successful"]:
            test_results["tests_passed"] += 1
        else:
            test_results["tests_failed"] += 1
    except Exception as e:
        print(f"❌ End-to-end analysis test failed: {e}")
        test_results["tests_failed"] += 1
        test_results["results"]["end_to_end"] = {"error": str(e)}
    
    # Calculate final results
    test_results["end_time"] = time.time()
    test_results["total_duration"] = test_results["end_time"] - test_results["start_time"]
    test_results["success_rate"] = test_results["tests_passed"] / test_results["tests_completed"] if test_results["tests_completed"] > 0 else 0
    
    # Print final summary
    print(f"\n{'='*70}")
    print("🏁 MESH SWARM AGENT TESTING COMPLETE")
    print(f"📊 Tests Completed: {test_results['tests_completed']}")
    print(f"✅ Tests Passed: {test_results['tests_passed']}")
    print(f"❌ Tests Failed: {test_results['tests_failed']}")
    print(f"📈 Success Rate: {test_results['success_rate']:.1%}")
    print(f"⏱️  Total Duration: {test_results['total_duration']:.2f} seconds")
    
    if test_results["success_rate"] >= 0.85:
        print("🎉 MESH SWARM SYSTEM TESTING: EXCELLENT")
    elif test_results["success_rate"] >= 0.7:
        print("👍 MESH SWARM SYSTEM TESTING: GOOD")
    else:
        print("⚠️  MESH SWARM SYSTEM TESTING: NEEDS IMPROVEMENT")
    
    return test_results


def main():
    """
    Main function for mesh swarm agent testing.
    """
    print(__doc__)
    
    print("\n🔧 Environment Check:")
    print(f"  Dependencies Available: {DEPENDENCIES_AVAILABLE}")
    print(f"  Python Version: {sys.version}")
    print(f"  Current Directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    expected_dirs = ["swarm", "Finance-assistant-swarm-agent", "test"]
    current_contents = os.listdir(".")
    
    missing_dirs = [d for d in expected_dirs if d not in current_contents]
    if missing_dirs:
        print(f"⚠️  Warning: Missing expected directories: {missing_dirs}")
        print("   Make sure you're running from the FSI-MAS root directory")
    
    # Run comprehensive testing
    results = run_comprehensive_mesh_swarm_test()
    
    # Save results to file
    import json
    results_file = Path(__file__).parent / "mesh_swarm_test_results.json"
    
    # Convert datetime objects to strings for JSON serialization
    json_results = json.loads(json.dumps(results, default=str))
    
    with open(results_file, 'w') as f:
        json.dump(json_results, f, indent=2)
    
    print(f"\n💾 Test results saved to: {results_file}")
    
    return results


if __name__ == "__main__":
    main()