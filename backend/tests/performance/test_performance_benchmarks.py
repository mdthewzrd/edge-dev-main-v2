"""
Performance Benchmark Tests for RENATA V2 Tools

Tests tool performance under various load conditions
Phase 3: Tool Testing - Task 3.2: Performance Benchmarking
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time

# Import all 13 tools
from tools.v31_scanner_generator import v31_scanner_generator
from tools.v31_validator import v31_validator
from tools.scanner_executor import scanner_executor
from tools.indicator_calculator import indicator_calculator
from tools.market_structure_analyzer import market_structure_analyzer
from tools.daily_context_detector import daily_context_detector
from tools.a_plus_analyzer import a_plus_analyzer
from tools.quick_backtester import quick_backtester
from tools.parameter_optimizer import parameter_optimizer
from tools.sensitivity_analyzer import sensitivity_analyzer
from tools.backtest_generator import backtest_generator
from tools.backtest_analyzer import backtest_analyzer
from tools.build_plan_generator import build_plan_generator
from tools.tool_types import ToolStatus


def generate_large_ohlcv_data(rows=10000):
    """Generate large OHLCV dataset for performance testing"""
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=rows, freq='D')

    # Generate realistic price data with trends
    base_price = 100
    trend = np.linspace(0, 0.5, rows)  # Upward trend
    noise = np.random.normal(0, 0.02, rows)
    returns = trend + noise

    # Add some volatility clustering
    volatility = np.random.uniform(0.01, 0.05, rows)
    returns = returns * volatility

    closes = base_price * (1 + returns).cumprod()

    df = pd.DataFrame({
        'date': dates,
        'open': closes * (1 + np.random.uniform(-0.01, 0.01, rows)),
        'high': closes * (1 + np.random.uniform(0, 0.02, rows)),
        'low': closes * (1 - np.random.uniform(0, 0.02, rows)),
        'close': closes,
        'volume': np.random.randint(1000000, 50000000, rows)
    })

    return df


def generate_large_scanner_results(num_trades=1000):
    """Generate large scanner results dataset"""
    trades = []
    np.random.seed(42)

    for i in range(num_trades):
        entry_price = 100 + np.random.uniform(-20, 20)
        exit_price = entry_price * (1 + np.random.uniform(-0.05, 0.08))

        trades.append({
            'date': f'2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}',
            'ticker': f'STOCK{np.random.randint(1, 100):04d}',
            'entry_price': entry_price,
            'exit_price': exit_price,
            'return': ((exit_price - entry_price) / entry_price)
        })

    return pd.DataFrame(trades)


def benchmark_v31_scanner_generator():
    """Benchmark: V31 Scanner Generator"""
    print("\n🚀 Benchmark: v31_scanner_generator")

    result = v31_scanner_generator({
        "description": "High-performance gap scanner with EMA confirmation and volume validation",
        "parameters": {
            "setup_type": "BACKSIDE_B",
            "min_gap_percent": 2.0,
            "target_percent": 3.0
        }
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.002 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.002s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.002


def benchmark_v31_validator():
    """Benchmark: V31 Validator"""
    print("\n🚀 Benchmark: v31_validator")

    # Generate a scanner first
    scanner_result = v31_scanner_generator({
        "description": "Test scanner for validation",
        "parameters": {"setup_type": "BACKSIDE_B"}
    })

    result = v31_validator({
        "scanner_code": scanner_result.result["scanner_code"],
        "strict_mode": False
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.001 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.001s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.001


def benchmark_indicator_calculator_small():
    """Benchmark: Indicator Calculator - Small Dataset (100 rows)"""
    print("\n🚀 Benchmark: indicator_calculator (Small: 100 rows)")

    df = generate_large_ohlcv_data(100)

    result = indicator_calculator({
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud"]
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.01 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.01s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.01


def benchmark_indicator_calculator_large():
    """Benchmark: Indicator Calculator - Large Dataset (10,000 rows)"""
    print("\n🚀 Benchmark: indicator_calculator (Large: 10,000 rows)")

    df = generate_large_ohlcv_data(10000)

    result = indicator_calculator({
        "ticker": "SPY",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud"]
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.5 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.5s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.5


def benchmark_market_structure_analyzer():
    """Benchmark: Market Structure Analyzer"""
    print("\n🚀 Benchmark: market_structure_analyzer (5,000 rows)")

    df = generate_large_ohlcv_data(5000)

    result = market_structure_analyzer({
        "ticker": "AAPL",
        "df": df,
        "pivot_lookback": 10,
        "trend_lookback": 20
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.1 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.1s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.1


def benchmark_quick_backtester():
    """Benchmark: Quick Backtester"""
    print("\n🚀 Benchmark: quick_backtester (1,000 trades)")

    scanner_results = generate_large_scanner_results(1000)

    result = quick_backtester({
        "scanner_results": scanner_results,
        "entry_price_col": "entry_price",
        "exit_price_col": "exit_price",
        "date_col": "date"
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.05 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.05s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.05


def benchmark_backtest_analyzer():
    """Benchmark: Backtest Analyzer"""
    print("\n🚀 Benchmark: backtest_analyzer (1,000 trades)")

    scanner_results = generate_large_scanner_results(1000)

    result = backtest_analyzer({
        "backtest_results": scanner_results,
        "initial_capital": 100000,
        "benchmark_return": 0.10
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.05 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Performance: {perf} (Target: <0.05s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.05


def benchmark_parameter_optimizer():
    """Benchmark: Parameter Optimizer"""
    print("\n🚀 Benchmark: parameter_optimizer")

    df = generate_large_ohlcv_data(1000)

    def test_strategy(df, gap_percent=2.0):
        df_copy = df.copy()
        df_copy["gap"] = ((df_copy["open"] - df_copy["close"].shift(1)) / df_copy["close"].shift(1) * 100)
        return len(df_copy[df_copy["gap"] > gap_percent])

    result = parameter_optimizer({
        "scanner_function": test_strategy,
        "parameter_ranges": {
            "gap_percent": [1.5, 2.0, 2.5, 3.0]
        },
        "evaluation_data": df,
        "metric": "signal_count",
        "max_iterations": 20
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 1.0 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Combinations tested: {result.result.get('combinations_tested', 'N/A')}")
    print(f"   Performance: {perf} (Target: <1.0s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 1.0


def benchmark_sensitivity_analyzer():
    """Benchmark: Sensitivity Analyzer"""
    print("\n🚀 Benchmark: sensitivity_analyzer")

    df = generate_large_ohlcv_data(1000)

    def test_strategy(df, gap_percent=2.0, volume_ratio=1.2):
        df_copy = df.copy()
        df_copy["gap"] = ((df_copy["open"] - df_copy["close"].shift(1)) / df_copy["close"].shift(1) * 100)
        df_copy["volume_ma"] = df_copy["volume"].rolling(20).mean()
        df_copy["volume_ratio"] = df_copy["volume"] / df_copy["volume_ma"]
        signals = df_copy[(df_copy["gap"] > gap_percent) & (df_copy["volume_ratio"] > volume_ratio)]
        return len(signals)

    result = sensitivity_analyzer({
        "scanner_function": test_strategy,
        "base_parameters": {"gap_percent": 2.0, "volume_ratio": 1.2},
        "parameter_variations": {"gap_percent": 0.3, "volume_ratio": 0.2},
        "evaluation_data": df
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.5 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Robustness Score: {result.result.get('robustness_score', 'N/A')}/100")
    print(f"   Performance: {perf} (Target: <0.5s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.5


def benchmark_a_plus_analyzer():
    """Benchmark: A+ Analyzer"""
    print("\n🚀 Benchmark: a_plus_analyzer (100 examples)")

    # Generate scanner first
    scanner_result = v31_scanner_generator({
        "description": "Test scanner",
        "parameters": {"setup_type": "BACKSIDE_B"}
    })

    # Generate 100 A+ examples
    a_plus_examples = []
    for i in range(100):
        a_plus_examples.append({
            "date": f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}",
            "setup_type": "BACKSIDE_B",
            "gap_percent": round(np.random.uniform(2.0, 5.0), 2),
            "ticker": f"STOCK{i:04d}"
        })

    result = a_plus_analyzer({
        "scanner_code": scanner_result.result["scanner_code"],
        "a_plus_examples": a_plus_examples,
        "strict_mode": False
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.5 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Examples analyzed: {len(a_plus_examples)}")
    print(f"   Performance: {perf} (Target: <0.5s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.5


def benchmark_backtest_generator():
    """Benchmark: Backtest Generator"""
    print("\n🚀 Benchmark: backtest_generator")

    scanner_result = v31_scanner_generator({
        "description": "Scanner for backtest generation",
        "parameters": {"setup_type": "BACKSIDE_B"}
    })

    result = backtest_generator({
        "scanner_code": scanner_result.result["scanner_code"],
        "backtest_config": {
            "initial_capital": 100000,
            "start_date": "2020-01-01",
            "end_date": "2024-12-31"
        }
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.01 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Code generated: {len(result.result.get('backtest_code', ''))} chars")
    print(f"   Performance: {perf} (Target: <0.01s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.01


def benchmark_build_plan_generator():
    """Benchmark: Build Plan Generator"""
    print("\n🚀 Benchmark: build_plan_generator")

    result = build_plan_generator({
        "strategy_description": "Complex multi-setup strategy combining gap analysis, trend following, momentum indicators, and comprehensive backtesting",
        "setup_types": ["BACKSIDE_B", "D2", "MDR", "FBO"],
        "complexity_level": "complex",
        "include_tool_recommendations": True,
        "include_testing_strategy": True,
        "include_validation_checkpoints": True
    })

    time_taken = result.execution_time
    status = "✅ PASS" if result.status == ToolStatus.SUCCESS else "❌ FAIL"
    perf = "✅ EXCELLENT" if time_taken < 0.001 else "⚠️ SLOW"

    print(f"   Status: {status}")
    print(f"   Time: {time_taken:.4f}s")
    print(f"   Implementation Steps: {len(result.result.get('implementation_steps', []))}")
    print(f"   Tool Recommendations: {len(result.result.get('tool_recommendations', []))}")
    print(f"   Performance: {perf} (Target: <0.001s)")

    return result.status == ToolStatus.SUCCESS and time_taken < 0.001


def run_all_benchmarks():
    """Run all performance benchmarks"""

    print("=" * 70)
    print("🚀 RENATA V2 PERFORMANCE BENCHMARK SUITE")
    print("=" * 70)
    print("\nTesting tool performance under various load conditions...")
    print("Target: All tools complete within specified time limits")

    benchmarks = [
        ("V31 Scanner Generator", benchmark_v31_scanner_generator),
        ("V31 Validator", benchmark_v31_validator),
        ("Indicator Calculator (Small)", benchmark_indicator_calculator_small),
        ("Indicator Calculator (Large)", benchmark_indicator_calculator_large),
        ("Market Structure Analyzer", benchmark_market_structure_analyzer),
        ("Quick Backtester", benchmark_quick_backtester),
        ("Backtest Analyzer", benchmark_backtest_analyzer),
        ("Parameter Optimizer", benchmark_parameter_optimizer),
        ("Sensitivity Analyzer", benchmark_sensitivity_analyzer),
        ("A+ Analyzer", benchmark_a_plus_analyzer),
        ("Backtest Generator", benchmark_backtest_generator),
        ("Build Plan Generator", benchmark_build_plan_generator),
    ]

    passed = 0
    failed = 0
    results = []

    for name, benchmark_func in benchmarks:
        try:
            if benchmark_func():
                passed += 1
                results.append((name, "✅ PASS"))
            else:
                failed += 1
                results.append((name, "❌ FAIL"))
        except Exception as e:
            failed += 1
            results.append((name, f"💥 ERROR: {e}"))

    print("\n" + "=" * 70)
    print("📊 PERFORMANCE BENCHMARK RESULTS")
    print("=" * 70)
    print(f"✅ Passed: {passed}/{len(benchmarks)}")
    print(f"❌ Failed: {failed}/{len(benchmarks)}")
    print(f"📊 Success Rate: {passed/len(benchmarks)*100:.1f}%")

    print("\n" + "-" * 70)
    print("DETAILED RESULTS:")
    print("-" * 70)

    for name, result in results:
        print(f"{name:40s} {result}")

    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_benchmarks()
    sys.exit(0 if success else 1)
