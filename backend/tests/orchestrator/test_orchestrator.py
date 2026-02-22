"""
Test Suite for RENATA V2 Orchestrator Agent

Tests the AI orchestrator that coordinates all 13 tools
Phase 4: Agent Integration - Task 4.1
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from orchestrator.renata_orchestrator import RenataOrchestrator, process_user_request


def create_sample_context():
    """Create sample context for testing"""
    dates = pd.date_range('2024-01-01', periods=100, freq='D')

    df = pd.DataFrame({
        'date': dates,
        'open': np.random.uniform(90, 110, 100),
        'high': np.random.uniform(90, 110, 100),
        'low': np.random.uniform(90, 110, 100),
        'close': np.random.uniform(90, 110, 100),
        'volume': np.random.randint(1000000, 10000000, 100)
    })

    return {
        "df": df,
        "ticker": "AAPL"
    }


def test_orchestrator_scanner_generation():
    """Test: Orchestrator generates scanner"""
    print("\n🧪 Test 1: Scanner Generation")

    orchestrator = RenataOrchestrator()
    result = orchestrator.process_request("Generate a Backside B gap scanner")

    assert result["success"] == True
    assert "V31 Scanner Generator" in result["tools_used"]
    assert "V31 Validator" in result["tools_used"]
    assert result["execution_time"] < 0.1

    print(f"   ✅ Scanner generated successfully")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_market_analysis():
    """Test: Orchestrator analyzes market"""
    print("\n🧪 Test 2: Market Analysis")

    orchestrator = RenataOrchestrator()
    context = create_sample_context()

    result = orchestrator.process_request(
        "Calculate 72/89 cloud and analyze market structure",
        context=context
    )

    # Should succeed with context
    assert "Indicator Calculator" in result["tools_used"]
    assert "Market Structure Analyzer" in result["tools_used"]

    print(f"   ✅ Analysis completed")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_optimization():
    """Test: Orchestrator optimizes parameters"""
    print("\n🧪 Test 3: Parameter Optimization")

    orchestrator = RenataOrchestrator()

    result = orchestrator.process_request(
        "Optimize gap parameters between 1.5 and 3.0"
    )

    assert "Parameter Optimizer" in result["tools_used"]
    assert "Sensitivity Analyzer" in result["tools_used"]

    print(f"   ✅ Optimization completed")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_backtest():
    """Test: Orchestrator runs backtest"""
    print("\n🧪 Test 4: Backtest")

    orchestrator = RenataOrchestrator()

    # Create scanner results
    scanner_results = pd.DataFrame([
        {'date': '2024-01-01', 'entry_price': 100, 'exit_price': 103, 'return': 0.03},
        {'date': '2024-01-02', 'entry_price': 102, 'exit_price': 104, 'return': 0.02}
    ])

    context = {
        "scanner_results": scanner_results
    }

    result = orchestrator.process_request(
        "Backtest these results",
        context=context
    )

    assert "Quick Backtester" in result["tools_used"]
    assert "Backtest Analyzer" in result["tools_used"]

    print(f"   ✅ Backtest completed")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_planning():
    """Test: Orchestrator creates implementation plan"""
    print("\n🧪 Test 5: Build Plan")

    orchestrator = RenataOrchestrator()

    result = orchestrator.process_request(
        "Create implementation plan for momentum strategy with D2 and MDR setups"
    )

    assert result["success"] == True
    assert "Build Plan Generator" in result["tools_used"]

    print(f"   ✅ Plan generated")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_multi_tool_workflow():
    """Test: Orchestrator handles complex multi-tool request"""
    print("\n🧪 Test 6: Multi-Tool Workflow")

    orchestrator = RenataOrchestrator()
    context = create_sample_context()

    result = orchestrator.process_request(
        "Generate a gap scanner, validate it, and analyze AAPL",
        context=context
    )

    # Should use multiple tools
    assert len(result["tools_used"]) >= 2

    print(f"   ✅ Multi-tool workflow completed")
    print(f"   📊 Tools used: {len(result['tools_used'])}")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_orchestrator_error_handling():
    """Test: Orchestrator handles errors gracefully"""
    print("\n🧪 Test 7: Error Handling")

    orchestrator = RenataOrchestrator()

    # Invalid request
    result = orchestrator.process_request("")

    # Should not crash
    assert "response" in result

    print(f"   ✅ Error handled gracefully")
    print(f"   📄 Response: {result['response'][:50]}...")
    print(f"   ⏱️ Time: {result['execution_time']:.4f}s")

    return True


def test_convenience_function():
    """Test: Convenience function for direct usage"""
    print("\n🧪 Test 8: Convenience Function")

    result = process_user_request("Generate a D2 trend scanner")

    assert "response" in result
    assert "tools_used" in result
    assert "execution_time" in result

    print(f"   ✅ Convenience function works")
    print(f"   🔧 Tools: {', '.join(result['tools_used'])}")

    return True


def run_all_orchestrator_tests():
    """Run all orchestrator tests"""

    print("=" * 70)
    print("🤖 RENATA V2 ORCHESTRATOR TEST SUITE")
    print("=" * 70)

    tests = [
        ("Scanner Generation", test_orchestrator_scanner_generation),
        ("Market Analysis", test_orchestrator_market_analysis),
        ("Parameter Optimization", test_orchestrator_optimization),
        ("Backtest", test_orchestrator_backtest),
        ("Build Plan", test_orchestrator_planning),
        ("Multi-Tool Workflow", test_orchestrator_multi_tool_workflow),
        ("Error Handling", test_orchestrator_error_handling),
        ("Convenience Function", test_convenience_function),
    ]

    passed = 0
    failed = 0
    errors = []

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"\n   ❌ FAILED: {test_name}")
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"\n   💥 ERROR: {test_name} - {e}")

    print("\n" + "=" * 70)
    print("📊 ORCHESTRATOR TEST RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(tests)} ({passed/len(tests)*100:.1f}%)")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if errors:
        print("\n❌ Failed Tests:")
        for test_name, error in errors:
            print(f"   • {test_name}")

    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_orchestrator_tests()
    sys.exit(0 if success else 1)
