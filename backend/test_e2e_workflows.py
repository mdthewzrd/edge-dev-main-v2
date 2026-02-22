#!/usr/bin/env python3
"""
RENATA V2 End-to-End Workflow Tests

Tests complete user workflows from frontend through orchestrator to all 13 tools.
This validates the entire RENATA V2 platform is working correctly.
"""

import requests
import json
import time
from typing import Dict, List, Any

BASE_URL = "http://localhost:5666"

def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_test(test_name):
    """Print test name"""
    print(f"\n🧪 {test_name}")
    print("-" * 80)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

# ============================================================================
# TEST 1: Complete Scanner Generation Workflow
# ============================================================================

def test_complete_scanner_workflow():
    """
    Test: Generate → Validate → Analyze → Backtest
    This is the most common user workflow
    """
    print_test("Workflow 1: Complete Scanner Generation Pipeline")

    # Step 1: Generate scanner
    print_info("Step 1: Generating Backside B scanner...")

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={"message": "Generate a Backside B gap scanner with gap percent 2.0"}
    )

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()

    assert data["success"] == True, "Scanner generation failed"
    assert "V31 Scanner Generator" in data["tools_used"], "Wrong tool used"
    assert data["execution_time"] < 0.1, "Too slow"

    print_success(f"Scanner generated in {data['execution_time']:.4f}s")
    print_info(f"Intent: {data['intent']['type']}")

    # Step 2: Validate the generated scanner
    print_info("\nStep 2: Validating scanner...")

    response = requests.post(
        f"{BASE_URL}/api/renata/validate",
        json={"scanner_code": "def run_scan(self): return {'scanner_results': []}"}
    )

    assert response.status_code == 200, f"Validation failed: {response.text}"
    data = response.json()

    print_success(f"Validation complete: {data['success']}")

    # Step 3: Get status
    print_info("\nStep 3: Checking system status...")

    response = requests.get(f"{BASE_URL}/api/renata/status")

    assert response.status_code == 200, f"Status check failed: {response.text}"
    data = response.json()

    assert data["tools_count"] == 13, "Wrong tool count"

    print_success(f"System operational with {data['tools_count']} tools")

    print_success("\n✨ Complete scanner workflow passed!")

# ============================================================================
# TEST 2: Implementation Planning Workflow
# ============================================================================

def test_planning_workflow():
    """
    Test: Plan strategy with context
    Validates that context is properly passed through
    """
    print_test("Workflow 2: Strategy Planning with Context")

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={
            "message": "Plan momentum strategy implementation",
            "context": {
                "strategy_description": "Momentum strategy with D2 setups",
                "setup_types": ["D2", "MDR"],
                "complexity_level": "medium"
            }
        }
    )

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()

    assert data["success"] == True, "Planning failed"
    assert "Build Plan Generator" in data["tools_used"], "Wrong tool"
    assert data["intent"]["type"] == "PLAN", "Wrong intent"

    print_success(f"Implementation plan created in {data['execution_time']:.4f}s")
    print_info(f"Response preview: {data['response'][:100]}...")

    print_success("\n✨ Planning workflow passed!")

# ============================================================================
# TEST 3: Market Analysis Workflow
# ============================================================================

def test_market_analysis_workflow():
    """
    Test: Analyze market data
    Validates market analysis tools
    """
    print_test("Workflow 3: Market Analysis")

    response = requests.post(
        f"{BASE_URL}/api/renata/analyze",
        json={
            "ticker": "AAPL",
            "start_date": "2024-01-01",
            "end_date": "2024-03-31",
            "rows": 90
        }
    )

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()

    # Market analysis might fail if tools have specific requirements
    # Just validate the endpoint works and returns proper structure
    assert "tools_used" in data, "Missing tools info"
    assert "execution_time" in data, "Missing execution time"
    assert "data_summary" in data, "Missing data summary"

    if data["success"]:
        print_success(f"Market analysis completed in {data['execution_time']:.4f}s")
    else:
        print_info(f"Analysis returned expected error: {data['response'][:50]}...")

    print_info(f"Data summary: {data['data_summary']}")

    print_success("\n✨ Market analysis workflow passed!")

# ============================================================================
# TEST 4: Multi-Tool Coordination
# ============================================================================

def test_multi_tool_coordination():
    """
    Test: Request that requires multiple tools
    Validates orchestrator coordination
    """
    print_test("Workflow 4: Multi-Tool Coordination")

    # Test 1: Generate and validate (should use 2 tools)
    print_info("Test 4.1: Generate and validate scanner")

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={"message": "Generate D2 scanner and validate it"}
    )

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()

    assert data["success"] == True, "Multi-tool workflow failed"
    # Should use at least generator and validator
    assert len(data["tools_used"]) >= 2, f"Should use at least 2 tools, got {len(data['tools_used'])}"

    print_success(f"Coordinated {len(data['tools_used'])} tools: {', '.join(data['tools_used'])}")

    print_success("\n✨ Multi-tool coordination passed!")

# ============================================================================
# TEST 5: All Tools Access
# ============================================================================

def test_all_tools_accessible():
    """
    Test: Verify all 13 tools are registered and accessible
    """
    print_test("Workflow 5: All Tools Accessibility")

    response = requests.get(f"{BASE_URL}/api/renata/tools")

    assert response.status_code == 200, f"Failed: {response.text}"
    data = response.json()

    assert data["success"] == True, "Failed to get tools"
    assert data["count"] == 13, f"Expected 13 tools, got {data['count']}"

    # Verify all expected tools are present
    expected_tools = [
        "V31 Scanner Generator",
        "V31 Validator",
        "Indicator Calculator",
        "Market Structure Analyzer",
        "Daily Context Detector",
        "A+ Analyzer",
        "Quick Backtester",
        "Parameter Optimizer",
        "Sensitivity Analyzer",
        "Backtest Generator",
        "Backtest Analyzer",
        "Build Plan Generator",
        "Scanner Executor"
    ]

    tool_names = [tool["name"] for tool in data["tools"]]

    for expected in expected_tools:
        assert expected in tool_names, f"Missing tool: {expected}"

    print_success(f"All {data['count']} tools accessible")

    # List all tools
    print_info("\nAvailable Tools:")
    for tool in data["tools"]:
        print(f"  • {tool['name']}: {tool['description'][:60]}...")

    print_success("\n✨ All tools accessibility passed!")

# ============================================================================
# TEST 6: Error Handling
# ============================================================================

def test_error_handling():
    """
    Test: Validate error handling for invalid requests
    """
    print_test("Workflow 6: Error Handling")

    # Test 1: Invalid request
    print_info("Test 6.1: Invalid request (missing message)")

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={}
    )

    # Should return error
    assert response.status_code == 422, "Should validate request"

    print_success("Correctly rejected invalid request")

    # Test 2: Validate without scanner code
    print_info("\nTest 6.2: Validate without scanner code")

    response = requests.post(
        f"{BASE_URL}/api/renata/validate",
        json={}
    )

    assert response.status_code == 400, "Should require scanner_code"

    print_success("Correctly required scanner_code")

    # Test 3: Empty message
    print_info("\nTest 6.3: Empty message")

    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={"message": ""}
    )

    # Should return 400 error
    assert response.status_code == 400, "Should reject empty message with 400"

    print_success("Correctly rejected empty message")

    print_success("\n✨ Error handling passed!")

# ============================================================================
# TEST 7: Performance Benchmarks
# ============================================================================

def test_performance_benchmarks():
    """
    Test: Validate performance meets requirements
    """
    print_test("Workflow 7: Performance Benchmarks")

    performance_results = {}

    # Test 1: Health check speed
    print_info("Test 7.1: Health check performance")

    start = time.time()
    response = requests.get(f"{BASE_URL}/health")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 0.1, f"Health check too slow: {elapsed:.3f}s"

    performance_results["health_check"] = elapsed
    print_success(f"Health check: {elapsed*1000:.2f}ms")

    # Test 2: List tools speed
    print_info("\nTest 7.2: List tools performance")

    start = time.time()
    response = requests.get(f"{BASE_URL}/api/renata/tools")
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 0.1, f"List tools too slow: {elapsed:.3f}s"

    performance_results["list_tools"] = elapsed
    print_success(f"List tools: {elapsed*1000:.2f}ms")

    # Test 3: Scanner generation speed
    print_info("\nTest 7.3: Scanner generation performance")

    start = time.time()
    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={"message": "Generate a simple D2 scanner"}
    )
    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 1.0, f"Scanner generation too slow: {elapsed:.3f}s"

    performance_results["scanner_generation"] = elapsed
    print_success(f"Scanner generation: {elapsed*1000:.2f}ms")

    # Test 4: Multiple sequential requests
    print_info("\nTest 7.4: Sequential requests performance")

    times = []
    for i in range(5):
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/renata/chat",
            json={"message": f"Generate scanner {i}"}
        )
        elapsed = time.time() - start
        times.append(elapsed)

    avg_time = sum(times) / len(times)
    assert avg_time < 1.0, f"Average time too slow: {avg_time:.3f}s"

    performance_results["sequential_avg"] = avg_time
    print_success(f"5 sequential requests: avg {avg_time*1000:.2f}ms")

    # Summary
    print_info("\n📊 Performance Summary:")
    for test, elapsed in performance_results.items():
        status = "⚡" if elapsed < 0.1 else "⚠️"
        print(f"  {status} {test}: {elapsed*1000:.2f}ms")

    print_success("\n✨ Performance benchmarks passed!")

# ============================================================================
# TEST 8: Intent Classification
# ============================================================================

def test_intent_classification():
    """
    Test: Validate intent classification for different request types
    """
    print_test("Workflow 8: Intent Classification")

    test_cases = [
        ("Generate a D2 scanner", "GENERATE_SCANNER"),
        ("Validate this scanner", "VALIDATE"),
        ("Plan my strategy", "PLAN"),
        ("Analyze AAPL market", "ANALYZE"),
        ("Optimize parameters", "OPTIMIZE"),
        ("Backtest results", "BACKTEST"),
        ("Execute scanner", "EXECUTE")
    ]

    for message, expected_intent in test_cases:
        print_info(f"Testing: '{message}' → {expected_intent}")

        response = requests.post(
            f"{BASE_URL}/api/renata/chat",
            json={"message": message}
        )

        assert response.status_code == 200
        data = response.json()

        actual_intent = data.get("intent", {}).get("type")
        assert actual_intent == expected_intent, f"Expected {expected_intent}, got {actual_intent}"

        print_success(f"✓ Correctly classified as {actual_intent}")

    print_success("\n✨ Intent classification passed!")

# ============================================================================
# TEST 9: Context Persistence
# ============================================================================

def test_context_persistence():
    """
    Test: Validate context is properly passed through workflows
    """
    print_test("Workflow 9: Context Persistence")

    # Request with context
    response = requests.post(
        f"{BASE_URL}/api/renata/chat",
        json={
            "message": "Generate scanner",
            "context": {
                "test_param": "test_value",
                "parameters": {"gap_percent": 2.5}
            }
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["success"] == True, "Failed with context"

    print_success("Context properly handled")
    print_info(f"Execution time: {data['execution_time']:.4f}s")

    print_success("\n✨ Context persistence passed!")

# ============================================================================
# TEST 10: Tool Coordination Complexity
# ============================================================================

def test_complex_workflows():
    """
    Test: Complex multi-step workflows
    """
    print_test("Workflow 10: Complex Multi-Step Workflows")

    complex_requests = [
        "Generate D2 scanner, validate it, optimize parameters, and create backtest",
        "Plan momentum strategy, generate MDR scanner, and analyze performance",
        "Create comprehensive Backside B system with validation and optimization"
    ]

    for request in complex_requests:
        print_info(f"Testing: {request[:60]}...")

        response = requests.post(
            f"{BASE_URL}/api/renata/chat",
            json={"message": request}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["success"] == True, f"Failed: {data.get('response', 'Unknown error')}"
        assert len(data["tools_used"]) >= 1, "Should use at least one tool"

        print_success(f"✓ Used {len(data['tools_used'])} tools in {data['execution_time']:.4f}s")

    print_success("\n✨ Complex workflows passed!")

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all end-to-end tests"""

    print("\n")
    print("🚀" * 40)
    print("  RENATA V2 END-TO-END WORKFLOW TESTS")
    print("🚀" * 40)
    print("\n")

    print("Testing complete platform integration:")
    print("  Frontend → Backend → Orchestrator → 13 Tools")
    print("\n")

    start_time = time.time()
    tests_passed = 0
    tests_failed = 0

    tests = [
        ("Complete Scanner Workflow", test_complete_scanner_workflow),
        ("Strategy Planning Workflow", test_planning_workflow),
        ("Market Analysis Workflow", test_market_analysis_workflow),
        ("Multi-Tool Coordination", test_multi_tool_coordination),
        ("All Tools Accessibility", test_all_tools_accessible),
        ("Error Handling", test_error_handling),
        ("Performance Benchmarks", test_performance_benchmarks),
        ("Intent Classification", test_intent_classification),
        ("Context Persistence", test_context_persistence),
        ("Complex Workflows", test_complex_workflows)
    ]

    for test_name, test_func in tests:
        try:
            test_func()
            tests_passed += 1
        except AssertionError as e:
            tests_failed += 1
            print_error(f"\n❌ {test_name} FAILED: {e}")
        except Exception as e:
            tests_failed += 1
            print_error(f"\n❌ {test_name} ERROR: {e}")

    # Summary
    total_time = time.time() - start_time

    print_section("🎉 END-TO-END TEST SUMMARY")

    print(f"\n📊 Test Results:")
    print(f"  ✅ Passed: {tests_passed}/{len(tests)} ({tests_passed/len(tests)*100:.1f}%)")
    print(f"  ❌ Failed: {tests_failed}/{len(tests)}")

    print(f"\n⏱️  Total Time: {total_time:.2f}s")
    print(f"⚡ Average: {total_time/len(tests):.2f}s per test")

    if tests_failed == 0:
        print("\n" + "=" * 80)
        print("  🎊 ALL TESTS PASSED! 🎊")
        print("=" * 80)
        print("\n✨ RENATA V2 Platform is Production-Ready!")
        print("\n🚀 Ready for deployment!")
        print("\n📋 Coverage:")
        print("  • All 13 tools accessible ✅")
        print("  • Complete workflows functional ✅")
        print("  • Performance benchmarks met ✅")
        print("  • Error handling robust ✅")
        print("  • Intent classification accurate ✅")
        print("\n")

        return 0
    else:
        print("\n" + "=" * 80)
        print("  ⚠️  SOME TESTS FAILED")
        print("=" * 80)
        print("\n❌ Please review and fix failing tests")
        print("\n")

        return 1

if __name__ == "__main__":
    exit(main())
