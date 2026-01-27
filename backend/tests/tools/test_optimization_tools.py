"""
Test Suite for Optimization Tools

Tests for:
1. parameter_optimizer - Grid search optimization
2. sensitivity_analyzer - Parameter sensitivity testing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tools to test
from tools.parameter_optimizer import parameter_optimizer
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.tool_types import ToolStatus


# Sample scanner function for testing
def sample_scanner(df, gap_threshold=0.8, volume_multiplier=1.5):
    """Sample scanner that filters based on parameters"""

    mask = (
        (df.get('gap_over_atr', 0) > gap_threshold) &
        (df.get('volume_ratio', 1) > volume_multiplier)
    )

    results = df[mask]

    if len(results) > 0:
        np.random.seed(42)
        results = results.copy()
        results['return'] = np.random.normal(0.02, 0.05, len(results))
    else:
        results = pd.DataFrame(columns=['gap_over_atr', 'volume_ratio', 'ticker', 'return'])

    return results


def test_parameter_optimizer_basic():
    """Test basic parameter optimization"""
    print("\n🧪 Test 1: parameter_optimizer - Basic Optimization")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8, 1.0],
            "volume_multiplier": [1.0, 1.5, 2.0]
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "max_iterations": 50
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "best_parameters" in result.result
    assert "best_metric_value" in result.result
    assert "combinations_tested" in result.result

    print(f"   ✅ Parameter optimization completed successfully")
    print(f"   🎯 Best Parameters: {result.result['best_parameters']}")
    print(f"   📊 Best Metric Value: {result.result['best_metric_value']:.4f}")
    print(f"   🔢 Combinations Tested: {result.result['combinations_tested']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_parameter_optimizer_win_rate_metric():
    """Test optimization with win_rate metric"""
    print("\n🧪 Test 2: parameter_optimizer - Win Rate Metric")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8, 1.0],
            "volume_multiplier": [1.0, 1.5, 2.0]
        },
        "evaluation_data": evaluation_data,
        "metric": "win_rate",
        "max_iterations": 20
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert result.result["optimization_metric"] == "win_rate"

    print(f"   ✅ Win rate optimization completed")
    print(f"   🎯 Best Win Rate: {result.result['best_metric_value']:.2%}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_parameter_optimizer_return_all_results():
    """Test returning all optimization results"""
    print("\n🧪 Test 3: parameter_optimizer - Return All Results")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8],
            "volume_multiplier": [1.0, 1.5]
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "return_all_results": True
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.SUCCESS
    all_results = result.result["all_results"]

    assert len(all_results) > 0
    assert len(all_results) <= 4  # 2 x 2 = 4 combinations max

    print(f"   ✅ All results returned correctly")
    print(f"   📊 Total Results: {len(all_results)}")
    print(f"   🔢 Combinations Tested: {result.result['combinations_tested']}")

    return True


def test_parameter_optimizer_validation():
    """Test input validation"""
    print("\n🧪 Test 4: parameter_optimizer - Validation")

    # Missing parameter_ranges
    input_data = {
        "evaluation_data": pd.DataFrame({'col': [1, 2, 3]})
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty parameter_ranges
    input_data = {
        "parameter_ranges": {},
        "evaluation_data": pd.DataFrame({'col': [1, 2, 3]})
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INVALID_INPUT"

    # Empty evaluation_data
    input_data = {
        "parameter_ranges": {"gap_threshold": [0.5, 0.8]},
        "evaluation_data": pd.DataFrame()
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INSUFFICIENT_DATA"

    print(f"   ✅ Input validation working correctly")

    return True


def test_parameter_optimizer_optimization_stats():
    """Test optimization statistics calculation"""
    print("\n🧪 Test 5: parameter_optimizer - Optimization Stats")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8, 1.0],
            "volume_multiplier": [1.0, 1.5]
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return"
    }

    result = parameter_optimizer(input_data)

    assert result.status == ToolStatus.SUCCESS
    stats = result.result["optimization_stats"]

    assert "mean_metric_value" in stats
    assert "std_metric_value" in stats
    assert "min_metric_value" in stats
    assert "max_metric_value" in stats

    print(f"   ✅ Optimization stats calculated correctly")
    print(f"   📊 Mean: {stats['mean_metric_value']:.4f}")
    print(f"   📊 Std: {stats['std_metric_value']:.4f}")
    print(f"   📊 Min: {stats['min_metric_value']:.4f}")
    print(f"   📊 Max: {stats['max_metric_value']:.4f}")

    return True


def test_sensitivity_analyzer_basic():
    """Test basic sensitivity analysis"""
    print("\n🧪 Test 6: sensitivity_analyzer - Basic Analysis")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 20,  # +/- 20%
            "volume_multiplier": 20
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return"
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "base_metric_value" in result.result
    assert "sensitivity_results" in result.result
    assert "robustness_score" in result.result

    print(f"   ✅ Sensitivity analysis completed successfully")
    print(f"   📊 Base Metric Value: {result.result['base_metric_value']:.4f}")
    print(f"   🛡️ Robustness Score: {result.result['robustness_score']:.2%}")
    print(f"   📈 Sensitive Parameters: {result.result['sensitive_parameters']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_sensitivity_analyzer_sensitivity_levels():
    """Test sensitivity level classification"""
    print("\n🧪 Test 7: sensitivity_analyzer - Sensitivity Levels")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 20,
            "volume_multiplier": 20
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "sensitivity_threshold": 0.2
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    sensitivity_results = result.result["sensitivity_results"]

    for r in sensitivity_results:
        assert r["sensitivity_level"] in ["HIGH", "MEDIUM", "LOW"]
        print(f"   {r['parameter']}: {r['sensitivity_level']} sensitivity")

    print(f"   ✅ Sensitivity levels classified correctly")

    return True


def test_sensitivity_analyzer_recommendation():
    """Test recommendation generation"""
    print("\n🧪 Test 8: sensitivity_analyzer - Recommendation")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 20,
            "volume_multiplier": 20
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return"
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    recommendation = result.result["recommendation"]

    assert isinstance(recommendation, str)
    assert len(recommendation) > 0

    print(f"   ✅ Recommendation generated correctly")
    print(f"   💡 Recommendation: {recommendation}")

    return True


def test_sensitivity_analyzer_validation():
    """Test input validation"""
    print("\n🧪 Test 9: sensitivity_analyzer - Validation")

    # Missing base_parameters
    input_data = {
        "parameter_variations": {},
        "evaluation_data": pd.DataFrame({'col': [1, 2, 3]})
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty base_parameters
    input_data = {
        "base_parameters": {},
        "parameter_variations": {"gap_threshold": 20},
        "evaluation_data": pd.DataFrame({'col': [1, 2, 3]})
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INVALID_INPUT"

    # Empty evaluation_data
    input_data = {
        "base_parameters": {"gap_threshold": 0.8},
        "parameter_variations": {"gap_threshold": 20},
        "evaluation_data": pd.DataFrame()
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INSUFFICIENT_DATA"

    print(f"   ✅ Input validation working correctly")

    return True


def test_sensitivity_analyzer_large_variations():
    """Test with large parameter variations"""
    print("\n🧪 Test 10: sensitivity_analyzer - Large Variations")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    input_data = {
        "scanner_function": sample_scanner,
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 50,  # +/- 50% (large variation)
            "volume_multiplier": 50
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "sensitivity_threshold": 0.3
    }

    result = sensitivity_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS

    # Larger variations should produce higher sensitivity
    for r in result.result["sensitivity_results"]:
        assert r["variation_pct"] == 50

    print(f"   ✅ Large variations handled correctly")
    print(f"   📊 Robustness Score: {result.result['robustness_score']:.2%}")

    return True


def test_performance_optimization_tools():
    """Performance test: Run both tools and measure execution time"""
    print("\n🚀 Test 11: Performance Test - Optimization Tools")

    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    times = []

    # Test 1: Parameter Optimizer
    start = datetime.now()
    parameter_optimizer({
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8, 1.0],
            "volume_multiplier": [1.0, 1.5, 2.0]
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "max_iterations": 50
    })
    times.append(("parameter_optimizer", (datetime.now() - start).total_seconds()))

    # Test 2: Sensitivity Analyzer
    start = datetime.now()
    sensitivity_analyzer({
        "scanner_function": sample_scanner,
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 20,
            "volume_multiplier": 20
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return"
    })
    times.append(("sensitivity_analyzer", (datetime.now() - start).total_seconds()))

    print("\n   ⚡ Performance Results:")
    total_time = 0
    for name, time_taken in times:
        print(f"      • {name}: {time_taken:.4f}s")
        total_time += time_taken

    print(f"\n   📊 Total execution time: {total_time:.4f}s")
    print(f"   📈 Average: {total_time / len(times):.4f}s")

    # Performance targets: <2s for parameter_optimizer, <1s for sensitivity_analyzer
    assert times[0][1] < 2.0, "parameter_optimizer too slow"
    assert times[1][1] < 1.0, "sensitivity_analyzer too slow"

    print(f"   ✅ All tools within performance targets")

    return True


def run_all_tests():
    """Run all tests and report results"""

    print("=" * 70)
    print("🧪 OPTIMIZATION TOOLS TEST SUITE")
    print("=" * 70)

    tests = [
        ("Parameter Optimizer - Basic Optimization", test_parameter_optimizer_basic),
        ("Parameter Optimizer - Win Rate Metric", test_parameter_optimizer_win_rate_metric),
        ("Parameter Optimizer - Return All Results", test_parameter_optimizer_return_all_results),
        ("Parameter Optimizer - Validation", test_parameter_optimizer_validation),
        ("Parameter Optimizer - Optimization Stats", test_parameter_optimizer_optimization_stats),
        ("Sensitivity Analyzer - Basic Analysis", test_sensitivity_analyzer_basic),
        ("Sensitivity Analyzer - Sensitivity Levels", test_sensitivity_analyzer_sensitivity_levels),
        ("Sensitivity Analyzer - Recommendation", test_sensitivity_analyzer_recommendation),
        ("Sensitivity Analyzer - Validation", test_sensitivity_analyzer_validation),
        ("Sensitivity Analyzer - Large Variations", test_sensitivity_analyzer_large_variations),
        ("Performance Test", test_performance_optimization_tools),
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
