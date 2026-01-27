"""
Test Suite for Build Plan Generator - FINAL TOOL!

Tests for build_plan_generator
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tool to test
from tools.build_plan_generator import build_plan_generator
from tools.tool_types import ToolStatus


def test_build_plan_generator_basic():
    """Test basic build plan generation"""
    print("\n🧪 Test 1: build_plan_generator - Basic Generation")

    test_input = {
        "strategy_description": "Momentum strategy that detects gap up continuations with EMA cloud confirmation",
        "setup_types": ["BACKSIDE_B", "D2"],
        "complexity_level": "medium"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    assert "strategy_name" in result.result
    assert "implementation_steps" in result.result
    assert "estimates" in result.result
    assert "tool_recommendations" in result.result

    print(f"   ✅ Build plan generated successfully")
    print(f"   📊 Strategy: {result.result['strategy_name']}")
    print(f"   🔨 Implementation Steps: {len(result.result['implementation_steps'])}")
    print(f"   🛠️ Tool Recommendations: {len(result.result['tool_recommendations'])}")
    print(f"   ⏱️ Estimates: {result.result['estimates']['total_hours']} hours")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_build_plan_generator_complex():
    """Test complex strategy plan"""
    print("\n🧪 Test 2: build_plan_generator - Complex Strategy")

    test_input = {
        "strategy_description": "Multi-setup strategy combining gap analysis, trend following, and momentum indicators with multi-timeframe analysis and comprehensive backtesting",
        "setup_types": ["BACKSIDE_B", "D2", "MDR", "FBO"],
        "complexity_level": "complex",
        "include_tool_recommendations": True,
        "include_testing_strategy": True,
        "include_validation_checkpoints": True
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    assert result.result["complexity_level"] == "complex"
    assert len(result.result["implementation_steps"]) > 5
    assert len(result.result["tool_recommendations"]) > 5

    print(f"   ✅ Complex strategy plan generated")
    print(f"   📊 Complexity: {result.result['complexity_level']}")
    print(f"   🔨 Steps: {len(result.result['implementation_steps'])}")
    print(f"   🛠️ Tools: {len(result.result['tool_recommendations'])}")

    return True


def test_build_plan_generator_simple():
    """Test simple strategy plan"""
    print("\n🧪 Test 3: build_plan_generator - Simple Strategy")

    test_input = {
        "strategy_description": "Simple gap up scanner",
        "setup_types": ["BACKSIDE_B"],
        "complexity_level": "simple"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    assert result.result["complexity_level"] == "simple"
    assert result.result["estimates"]["total_hours"] < 20  # Should be faster

    print(f"   ✅ Simple strategy plan generated")
    print(f"   📊 Total Hours: {result.result['estimates']['total_hours']}")
    print(f"   📅 Total Days: {result.result['estimates']['total_days']}")

    return True


def test_build_plan_generator_requirements_analysis():
    """Test requirements analysis"""
    print("\n🧪 Test 4: build_plan_generator - Requirements Analysis")

    test_input = {
        "strategy_description": "Strategy with gap detection, trend analysis using EMA, volume confirmation, and multi-timeframe support",
        "setup_types": ["BACKSIDE_B", "D2", "FBO"],
        "complexity_level": "complex"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    requirements = result.result["requirements"]

    assert requirements["has_gap_detection"] == True
    assert requirements["has_trend_detection"] == True
    assert requirements["has_volume_analysis"] == True
    assert requirements["has_multi_timeframe"] == True

    print(f"   ✅ Requirements analyzed correctly")
    print(f"   🔍 Gap Detection: {requirements['has_gap_detection']}")
    print(f"   📈 Trend Detection: {requirements['has_trend_detection']}")
    print(f"   📊 Volume Analysis: {requirements['has_volume_analysis']}")
    print(f"   ⏱️ Multi-timeframe: {requirements['has_multi_timeframe']}")

    return True


def test_build_plan_generator_tool_recommendations():
    """Test tool recommendations"""
    print("\n🧪 Test 5: build_plan_generator - Tool Recommendations")

    test_input = {
        "strategy_description": "Trend following strategy with EMA indicators",
        "setup_types": ["D2"],
        "complexity_level": "medium"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    recommendations = result.result["tool_recommendations"]

    assert len(recommendations) > 0

    # Verify core tools are always recommended
    tool_names = [r["tool"] for r in recommendations]
    assert "v31_scanner_generator" in tool_names
    assert "v31_validator" in tool_names

    print(f"   ✅ Tool recommendations generated")
    print(f"   🛠️ Total Recommendations: {len(recommendations)}")
    print(f"   📋 Tools: {', '.join(tool_names[:5])}...")

    return True


def test_build_plan_generator_implementation_steps():
    """Test implementation steps generation"""
    print("\n🧪 Test 6: build_plan_generator - Implementation Steps")

    test_input = {
        "strategy_description": "Gap momentum strategy",
        "setup_types": ["BACKSIDE_B"],
        "complexity_level": "medium",
        "include_testing_strategy": True,
        "include_validation_checkpoints": True
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    steps = result.result["implementation_steps"]

    assert len(steps) > 0

    # Verify step structure
    for step in steps:
        assert "step" in step
        assert "phase" in step
        assert "title" in step
        assert "description" in step
        assert "estimated_time" in step

    print(f"   ✅ Implementation steps generated")
    print(f"   🔢 Total Steps: {len(steps)}")

    phases = set(s["phase"] for s in steps)
    print(f"   📊 Phases: {', '.join(phases)}")

    return True


def test_build_plan_generator_validation_checkpoints():
    """Test validation checkpoints"""
    print("\n🧪 Test 7: build_plan_generator - Validation Checkpoints")

    test_input = {
        "strategy_description": "Strategy with backtesting",
        "setup_types": ["D2"],
        "complexity_level": "medium",
        "include_validation_checkpoints": True
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    checkpoints = result.result["validation_checkpoints"]

    assert len(checkpoints) > 0

    for checkpoint in checkpoints:
        assert "checkpoint" in checkpoint
        assert "criteria" in checkpoint

    print(f"   ✅ Validation checkpoints generated")
    print(f"   ✅ Total Checkpoints: {len(checkpoints)}")

    return True


def test_build_plan_generator_testing_strategy():
    """Test testing strategy generation"""
    print("\n🧪 Test 8: build_plan_generator - Testing Strategy")

    test_input = {
        "strategy_description": "Complex multi-setup strategy",
        "setup_types": ["BACKSIDE_B", "D2", "MDR"],
        "complexity_level": "complex",
        "include_testing_strategy": True
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    testing_strategy = result.result["testing_strategy"]

    assert testing_strategy is not None
    assert "test_cases" in testing_strategy
    assert "coverage_target" in testing_strategy

    print(f"   ✅ Testing strategy generated")
    print(f"   📊 Test Cases: {len(testing_strategy['test_cases'])}")
    print(f"   🎯 Coverage Target: {testing_strategy['coverage_target']}%")
    print(f"   ⚡ Priority: {testing_strategy['test_priority']}")

    return True


def test_build_plan_generator_estimates():
    """Test time estimates"""
    print("\n🧪 Test 9: build_plan_generator - Estimates")

    test_input = {
        "strategy_description": "Medium complexity strategy",
        "setup_types": ["BACKSIDE_B", "D2"],
        "complexity_level": "medium"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    estimates = result.result["estimates"]

    assert estimates["total_hours"] > 0
    assert estimates["total_days"] > 0
    assert estimates["development_hours"] > 0
    assert estimates["testing_hours"] > 0

    print(f"   ✅ Estimates calculated")
    print(f"   ⏱️ Total Hours: {estimates['total_hours']}")
    print(f"   📅 Total Days: {estimates['total_days']}")
    print(f"   🔨 Development: {estimates['development_hours']}h")
    print(f"   🧪 Testing: {estimates['testing_hours']}h")

    return True


def test_build_plan_generator_validation():
    """Test input validation"""
    print("\n🧪 Test 10: build_plan_generator - Validation")

    # Missing strategy_description
    input_data = {
        "setup_types": ["BACKSIDE_B"]
    }

    result = build_plan_generator(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Missing setup_types
    input_data = {
        "strategy_description": "Test strategy"
    }

    result = build_plan_generator(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Invalid complexity_level
    input_data = {
        "strategy_description": "Test strategy",
        "setup_types": ["BACKSIDE_B"],
        "complexity_level": "invalid"
    }

    result = build_plan_generator(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INVALID_INPUT"

    print(f"   ✅ Input validation working correctly")

    return True


def test_build_plan_generator_next_steps():
    """Test next steps generation"""
    print("\n🧪 Test 11: build_plan_generator - Next Steps")

    test_input = {
        "strategy_description": "Gap continuation strategy",
        "setup_types": ["BACKSIDE_B"],
        "complexity_level": "simple"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    next_steps = result.result["next_steps"]

    assert len(next_steps) > 0
    assert isinstance(next_steps, list)

    print(f"   ✅ Next steps generated")
    print(f"   📋 Steps: {len(next_steps)}")
    for step in next_steps:
        print(f"      • {step}")

    return True


def test_build_plan_generator_backtesting_included():
    """Test backtesting inclusion in plan"""
    print("\n🧪 Test 12: build_plan_generator - Backtesting Included")

    test_input = {
        "strategy_description": "Strategy with comprehensive backtesting",
        "setup_types": ["D2"],
        "complexity_level": "medium"
    }

    result = build_plan_generator(test_input)

    assert result.status == ToolStatus.SUCCESS
    steps = result.result["implementation_steps"]

    # Check if backtest steps are included
    has_backtest_step = any("backtest" in step["title"].lower() for step in steps)

    print(f"   ✅ Backtesting included: {has_backtest_step}")
    print(f"   🔨 Total Steps: {len(steps)}")

    return True


def test_performance_build_plan_generator():
    """Performance test"""
    print("\n🚀 Test 13: Performance Test - Build Plan Generator")

    start = datetime.now()

    build_plan_generator({
        "strategy_description": "Comprehensive strategy with gap analysis, trend detection, volume validation, and multi-setup support",
        "setup_types": ["BACKSIDE_B", "D2", "MDR", "FBO", "T30"],
        "complexity_level": "complex",
        "include_tool_recommendations": True,
        "include_testing_strategy": True,
        "include_validation_checkpoints": True
    })

    execution_time = (datetime.now() - start).total_seconds()

    print(f"   ⚡ Execution time: {execution_time:.4f}s")

    # Performance target: <0.5s
    assert execution_time < 0.5, "build_plan_generator too slow"

    print(f"   ✅ Performance target met (<0.5s)")

    return True


def run_all_tests():
    """Run all tests and report results"""

    print("=" * 70)
    print("🧪 BUILD PLAN GENERATOR TEST SUITE - FINAL TOOL!")
    print("=" * 70)

    tests = [
        ("Basic Generation", test_build_plan_generator_basic),
        ("Complex Strategy", test_build_plan_generator_complex),
        ("Simple Strategy", test_build_plan_generator_simple),
        ("Requirements Analysis", test_build_plan_generator_requirements_analysis),
        ("Tool Recommendations", test_build_plan_generator_tool_recommendations),
        ("Implementation Steps", test_build_plan_generator_implementation_steps),
        ("Validation Checkpoints", test_build_plan_generator_validation_checkpoints),
        ("Testing Strategy", test_build_plan_generator_testing_strategy),
        ("Estimates", test_build_plan_generator_estimates),
        ("Validation", test_build_plan_generator_validation),
        ("Next Steps", test_build_plan_generator_next_steps),
        ("Backtesting Included", test_build_plan_generator_backtesting_included),
        ("Performance Test", test_performance_build_plan_generator),
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
            print(f"   ❌ FAILED: {e}")
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"   💥 ERROR: {e}")

    print("\n" + "=" * 70)
    print("📊 TEST RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")

    if errors:
        print("\n❌ Failed Tests:")
        for test_name, error in errors:
            print(f"   • {test_name}: {error}")

    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
