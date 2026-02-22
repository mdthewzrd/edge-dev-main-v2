"""
Integration Tests for RENATA V2 Tool Workflows

Tests common tool combinations and workflows
Phase 3: Tool Testing - Task 3.2: Integration Testing
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tools to test
from tools.v31_scanner_generator import v31_scanner_generator
from tools.v31_validator import v31_validator
from tools.indicator_calculator import indicator_calculator
from tools.market_structure_analyzer import market_structure_analyzer
from tools.a_plus_analyzer import a_plus_analyzer
from tools.quick_backtester import quick_backtester
from tools.parameter_optimizer import parameter_optimizer
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.backtest_generator import backtest_generator
from tools.backtest_analyzer import backtest_analyzer
from tools.tool_types import ToolStatus


def create_sample_ohlcv():
    """Create sample OHLCV market data for testing"""
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')

    np.random.seed(42)
    base_price = 100
    returns = np.random.normal(0, 0.02, 100)
    closes = base_price * (1 + returns).cumprod()

    df = pd.DataFrame({
        'date': dates,
        'open': closes * (1 + np.random.uniform(-0.01, 0.01, 100)),
        'high': closes * (1 + np.random.uniform(0, 0.02, 100)),
        'low': closes * (1 - np.random.uniform(0, 0.02, 100)),
        'close': closes,
        'volume': np.random.randint(1000000, 10000000, 100)
    })

    return df


def create_scanner_results():
    """Create sample scanner results for backtesting"""
    trades = []
    np.random.seed(42)

    for i in range(10):
        entry_price = 100 + np.random.uniform(-5, 5)
        exit_price = entry_price * (1 + np.random.uniform(-0.02, 0.05))

        trades.append({
            'date': f'2024-01-{i+1:02d}',
            'ticker': 'TEST',
            'entry_price': entry_price,
            'exit_price': exit_price,
            'return': ((exit_price - entry_price) / entry_price)  # Decimal format
        })

    return pd.DataFrame(trades)


def test_scanner_workflow():
    """Test: Generate scanner → Validate scanner"""
    print("\n🧪 Test 1: Scanner Generation → Validation")

    # Step 1: Generate V31 scanner
    print("\n   Step 1: Generating V31 scanner...")
    scanner_result = v31_scanner_generator({
        "description": "Backside B setup scanner that detects gap up continuations with EMA cloud confirmation and volume validation",
        "parameters": {
            "setup_type": "BACKSIDE_B",
            "min_gap_percent": 2.0,
            "target_percent": 3.0
        }
    })

    assert scanner_result.status == ToolStatus.SUCCESS
    assert "scanner_code" in scanner_result.result
    print(f"   ✅ Scanner generated ({len(scanner_result.result['scanner_code'])} chars)")

    # Step 2: Validate the scanner
    print("\n   Step 2: Validating scanner...")
    validation_result = v31_validator({
        "scanner_code": scanner_result.result["scanner_code"],
        "strict_mode": False
    })

    assert validation_result.status == ToolStatus.SUCCESS
    assert "compliance_score" in validation_result.result
    print(f"   ✅ Scanner validated (Score: {validation_result.result['compliance_score']}/100)")

    print(f"\n   ✅ WORKFLOW COMPLETE")
    print(f"   ⏱️ Time: {scanner_result.execution_time + validation_result.execution_time:.4f}s")

    return True


def test_market_analysis_workflow():
    """Test: Calculate indicators → Analyze market structure"""
    print("\n🧪 Test 2: Market Analysis Workflow")

    df = create_sample_ohlcv()

    # Step 1: Calculate indicators
    print("\n   Step 1: Calculating indicators...")
    indicator_result = indicator_calculator({
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud"]
    })

    assert indicator_result.status == ToolStatus.SUCCESS
    assert "indicators" in indicator_result.result
    print(f"   ✅ Indicators calculated: {list(indicator_result.result['indicators'].keys())}")

    # Step 2: Analyze market structure
    print("\n   Step 2: Analyzing market structure...")
    structure_result = market_structure_analyzer({
        "ticker": "AAPL",
        "df": df,
        "pivot_lookback": 10,
        "trend_lookback": 20
    })

    assert structure_result.status == ToolStatus.SUCCESS
    assert "trend" in structure_result.result
    print(f"   ✅ Market structure analyzed (Trend: {structure_result.result['trend']['direction']})")

    print(f"\n   ✅ WORKFLOW COMPLETE")
    print(f"   ⏱️ Time: {indicator_result.execution_time + structure_result.execution_time:.4f}s")

    return True


def test_validation_workflow():
    """Test: A+ analyzer → Backtest generator"""
    print("\n🧪 Test 3: Validation Workflow")

    # Generate a simple scanner first
    scanner_result = v31_scanner_generator({
        "description": "Simple gap up scanner for backtesting",
        "parameters": {
            "setup_type": "BACKSIDE_B",
            "min_gap_percent": 2.0
        }
    })

    assert scanner_result.status == ToolStatus.SUCCESS
    scanner_code = scanner_result.result["scanner_code"]

    # Step 1: Validate against A+ examples
    print("\n   Step 1: A+ validation...")
    a_plus_result = a_plus_analyzer({
        "scanner_code": scanner_code,
        "a_plus_examples": [
            {
                "date": "2024-01-10",
                "setup_type": "BACKSIDE_B",
                "gap_percent": 2.5,
                "ticker": "AAPL"
            }
        ],
        "strict_mode": False
    })

    assert a_plus_result.status == ToolStatus.SUCCESS
    print(f"   ✅ A+ validation complete")

    # Step 2: Generate backtest code
    print("\n   Step 2: Generating backtest script...")
    backtest_gen_result = backtest_generator({
        "scanner_code": scanner_code,
        "backtest_config": {
            "initial_capital": 10000,
            "start_date": "2024-01-01",
            "end_date": "2024-12-31"
        }
    })

    assert backtest_gen_result.status == ToolStatus.SUCCESS
    assert "backtest_code" in backtest_gen_result.result
    print(f"   ✅ Backtest code generated ({len(backtest_gen_result.result['backtest_code'])} chars)")

    print(f"\n   ✅ WORKFLOW COMPLETE")
    print(f"   ⏱️ Time: {a_plus_result.execution_time + backtest_gen_result.execution_time:.4f}s")

    return True


def test_optimization_workflow():
    """Test: Parameter optimization → Sensitivity analysis"""
    print("\n🧪 Test 4: Optimization Workflow")

    df = create_sample_ohlcv()

    def test_strategy(df, gap_percent=2.0, volume_ratio=1.2):
        """Simple test strategy - note: data first, then params as kwargs"""
        df_copy = df.copy()
        df_copy["gap"] = ((df_copy["open"] - df_copy["close"].shift(1)) / df_copy["close"].shift(1) * 100)
        df_copy["volume_ma"] = df_copy["volume"].rolling(20).mean()
        df_copy["volume_ratio"] = df_copy["volume"] / df_copy["volume_ma"]
        signals = df_copy[(df_copy["gap"] > gap_percent) & (df_copy["volume_ratio"] > volume_ratio)]
        return len(signals)

    # Step 1: Optimize parameters
    print("\n   Step 1: Optimizing parameters...")
    opt_result = parameter_optimizer({
        "scanner_function": test_strategy,
        "parameter_ranges": {
            "gap_percent": [1.5, 2.0, 2.5],
            "volume_ratio": [1.0, 1.2, 1.5]
        },
        "evaluation_data": df,
        "metric": "signal_count"
    })

    assert opt_result.status == ToolStatus.SUCCESS
    best_params = opt_result.result["best_parameters"]
    print(f"   ✅ Optimization complete (Best params: {best_params})")

    # Step 2: Sensitivity analysis
    print("\n   Step 2: Running sensitivity analysis...")
    sens_result = sensitivity_analyzer({
        "scanner_function": test_strategy,
        "base_parameters": best_params,
        "parameter_variations": {
            "gap_percent": 0.3,
            "volume_ratio": 0.2
        },
        "evaluation_data": df
    })

    assert sens_result.status == ToolStatus.SUCCESS
    print(f"   ✅ Sensitivity complete (Robustness: {sens_result.result['robustness_score']}/100)")

    print(f"\n   ✅ WORKFLOW COMPLETE")
    print(f"   ⏱️ Time: {opt_result.execution_time + sens_result.execution_time:.4f}s")

    return True


def test_backtest_workflow():
    """Test: Scanner results → Quick backtest → Analysis"""
    print("\n🧪 Test 5: Backtest Workflow")

    scanner_results = create_scanner_results()

    # Step 1: Quick backtest validation
    print("\n   Step 1: Quick backtest...")
    qb_result = quick_backtester({
        "scanner_results": scanner_results,
        "entry_price_col": "entry_price",
        "exit_price_col": "exit_price",
        "date_col": "date"
    })

    assert qb_result.status == ToolStatus.SUCCESS
    # quick_backtester returns flat structure, not nested
    assert "total_return" in qb_result.result
    print(f"   ✅ Quick backtest (Return: {qb_result.result['total_return']:.2f}%)")

    # Step 2: Detailed analysis
    print("\n   Step 2: Detailed analysis...")
    analysis_result = backtest_analyzer({
        "backtest_results": scanner_results,
        "initial_capital": 10000,
        "benchmark_return": 0.02
    })

    assert analysis_result.status == ToolStatus.SUCCESS
    assert "return_metrics" in analysis_result.result
    print(f"   ✅ Analysis complete (Score: {analysis_result.result.get('overall_score', 'N/A')})")

    print(f"\n   ✅ WORKFLOW COMPLETE")
    print(f"   ⏱️ Time: {qb_result.execution_time + analysis_result.execution_time:.4f}s")

    return True


def test_error_handling():
    """Test error handling across tools"""
    print("\n🧪 Test 6: Error Handling")

    # Test 1: Invalid input to scanner generator
    print("\n   Test 1: Missing required parameter...")
    result = v31_scanner_generator({
        # Missing: description
        "parameters": {}
    })
    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"
    print(f"   ✅ Missing parameter detected")

    # Test 2: Invalid scanner code
    print("\n   Test 2: Invalid scanner code...")
    result = v31_validator({
        "scanner_code": "invalid {{{"
    })
    assert result.status == ToolStatus.ERROR
    print(f"   ✅ Invalid code rejected")

    # Test 3: Empty DataFrame
    print("\n   Test 3: Empty DataFrame...")
    result = indicator_calculator({
        "ticker": "TEST",
        "df": pd.DataFrame(),
        "indicators": ["72_89_cloud"]
    })
    assert result.status == ToolStatus.ERROR
    print(f"   ✅ Empty DataFrame rejected")

    print(f"\n   ✅ ERROR HANDLING COMPLETE")

    return True


def test_multi_tool_chain():
    """Test chaining multiple tools together"""
    print("\n🧪 Test 7: Multi-Tool Chain")

    df = create_sample_ohlcv()

    # Tool 1: Generate scanner
    print("\n   Step 1: Generate scanner...")
    scanner_result = v31_scanner_generator({
        "description": "Test scanner for AAPL",
        "parameters": {"setup_type": "BACKSIDE_B"}
    })
    assert scanner_result.status == ToolStatus.SUCCESS
    print(f"   ✅ Scanner generated")

    # Tool 2: Validate scanner
    print("\n   Step 2: Validate scanner...")
    validate_result = v31_validator({
        "scanner_code": scanner_result.result["scanner_code"],
        "strict_mode": False
    })
    assert validate_result.status == ToolStatus.SUCCESS
    print(f"   ✅ Scanner validated")

    # Tool 3: Calculate indicators
    print("\n   Step 3: Calculate indicators...")
    indicator_result = indicator_calculator({
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud"]
    })
    assert indicator_result.status == ToolStatus.SUCCESS
    print(f"   ✅ Indicators calculated")

    # Tool 4: Analyze structure
    print("\n   Step 4: Analyze structure...")
    structure_result = market_structure_analyzer({
        "ticker": "AAPL",
        "df": df,
        "pivot_lookback": 10
    })
    assert structure_result.status == ToolStatus.SUCCESS
    print(f"   ✅ Structure analyzed")

    print(f"\n   ✅ MULTI-TOOL CHAIN COMPLETE")
    total_time = (scanner_result.execution_time + validate_result.execution_time +
                  indicator_result.execution_time + structure_result.execution_time)
    print(f"   ⏱️ Total time: {total_time:.4f}s")

    return True


def run_all_tests():
    """Run all integration tests"""

    print("=" * 70)
    print("🧪 RENATA V2 INTEGRATION TEST SUITE")
    print("=" * 70)

    tests = [
        ("Scanner Workflow", test_scanner_workflow),
        ("Market Analysis Workflow", test_market_analysis_workflow),
        ("Validation Workflow", test_validation_workflow),
        ("Optimization Workflow", test_optimization_workflow),
        ("Backtest Workflow", test_backtest_workflow),
        ("Error Handling", test_error_handling),
        ("Multi-Tool Chain", test_multi_tool_chain),
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
            print(f"      {e}")
            import traceback
            traceback.print_exc()
        except Exception as e:
            failed += 1
            errors.append((test_name, str(e)))
            print(f"\n   💥 ERROR: {test_name}")
            print(f"      {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("📊 INTEGRATION TEST RESULTS")
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
    success = run_all_tests()
    sys.exit(0 if success else 1)
