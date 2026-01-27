"""
Test Suite for Backtest Tools

Tests for:
1. backtest_generator - Generate backtest code from scanner
2. backtest_analyzer - Analyze backtest results and metrics
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tools to test
from tools.backtest_generator import backtest_generator
from tools.backtest_analyzer import backtest_analyzer
from tools.tool_types import ToolStatus


# Sample scanner for testing
SAMPLE_SCANNER = """
def stage2_process_symbols(df):
    # Backside B setup
    gap = df['open'] - df['close'].shift(1)
    atr = calculate_atr(df, 14)
    gap_over_atr = gap / atr

    ema72 = df['close'].ewm(span=72).mean()
    ema89 = df['close'].ewm(span=89).mean()

    if gap_over_atr > 0.8 and df['close'].iloc[-1] > ema72.iloc[-1]:
        return {
            'setup_type': 'BACKSIDE_B',
            'entry_price': df['close'].iloc[-1]
        }

    return None
"""


def test_backtest_generator_basic():
    """Test basic backtest code generation"""
    print("\n🧪 Test 1: backtest_generator - Basic Generation")

    backtest_config = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000,
        "position_size": 0.02,
        "max_positions": 10
    }

    input_data = {
        "scanner_code": SAMPLE_SCANNER,
        "backtest_config": backtest_config,
        "include_comments": True,
        "include_visualization": False
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "backtest_code" in result.result
    assert "scanner_parameters" in result.result
    assert "code_stats" in result.result

    backtest_code = result.result["backtest_code"]

    # Verify code contains key sections
    assert "import pandas" in backtest_code
    assert "def run_backtest()" in backtest_code
    assert "def calculate_returns" in backtest_code
    assert "def calculate_performance_metrics" in backtest_code

    print(f"   ✅ Backtest code generated successfully")
    print(f"   📊 Code Lines: {result.result['code_stats']['total_lines']}")
    print(f"   📝 Code Chars: {result.result['code_stats']['estimated_chars']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_backtest_generator_with_visualization():
    """Test backtest generation with visualization code"""
    print("\n🧪 Test 2: backtest_generator - With Visualization")

    backtest_config = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000
    }

    input_data = {
        "scanner_code": SAMPLE_SCANNER,
        "backtest_config": backtest_config,
        "include_comments": True,
        "include_visualization": True
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.SUCCESS
    backtest_code = result.result["backtest_code"]

    # Verify visualization code is included
    assert "import matplotlib" in backtest_code
    assert "def plot_equity_curve" in backtest_code

    print(f"   ✅ Backtest code with visualization generated")
    print(f"   📊 Includes plotting functions")

    return True


def test_backtest_generator_without_comments():
    """Test backtest generation without comments"""
    print("\n🧪 Test 3: backtest_generator - No Comments")

    backtest_config = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000
    }

    input_data = {
        "scanner_code": SAMPLE_SCANNER,
        "backtest_config": backtest_config,
        "include_comments": False,
        "include_visualization": False
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.SUCCESS
    backtest_code = result.result["backtest_code"]

    # Verify fewer comment lines
    stats = result.result["code_stats"]
    print(f"   ✅ Code generated without comments")
    print(f"   📊 Comment Lines: {stats['comment_lines']}")

    return True


def test_backtest_generator_parameter_extraction():
    """Test scanner parameter extraction"""
    print("\n🧪 Test 4: backtest_generator - Parameter Extraction")

    backtest_config = {"start_date": "2023-01-01", "end_date": "2024-01-01"}

    input_data = {
        "scanner_code": SAMPLE_SCANNER,
        "backtest_config": backtest_config
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.SUCCESS
    params = result.result["scanner_parameters"]

    assert "setup_types" in params
    assert "indicators" in params
    assert "filters" in params

    print(f"   ✅ Parameters extracted successfully")
    print(f"   🎯 Setup Types: {params['setup_types']}")
    print(f"   📊 Indicators: {params['indicators']}")
    print(f"   🔍 Filters: {params['filters']}")

    return True


def test_backtest_generator_validation():
    """Test input validation"""
    print("\n🧪 Test 5: backtest_generator - Validation")

    # Missing scanner_code
    input_data = {
        "backtest_config": {}
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty scanner_code
    input_data = {
        "scanner_code": "",
        "backtest_config": {}
    }

    result = backtest_generator(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INVALID_INPUT"

    print(f"   ✅ Input validation working correctly")

    return True


def test_backtest_analyzer_basic():
    """Test basic backtest analysis"""
    print("\n🧪 Test 6: backtest_analyzer - Basic Analysis")

    # Generate sample backtest results
    np.random.seed(42)
    num_trades = 50
    returns = np.random.normal(0.02, 0.08, num_trades)

    backtest_results = pd.DataFrame({
        'ticker': [f'STOCK{i}' for i in range(num_trades)],
        'entry_price': np.random.uniform(100, 200, num_trades),
        'exit_price': np.random.uniform(100, 200, num_trades),
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "benchmark_return": 0.10,
        "include_drawdown_analysis": True,
        "include_trade_stats": True
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "return_metrics" in result.result
    assert "risk_metrics" in result.result
    assert "drawdown_analysis" in result.result
    assert "trade_statistics" in result.result
    assert "overall_score" in result.result

    print(f"   ✅ Backtest analysis completed successfully")
    print(f"   📊 Overall Score: {result.result['overall_score']}/100")
    print(f"   📈 Total Return: {result.result['return_metrics']['total_return']:.2%}")
    print(f"   🎯 Sharpe Ratio: {result.result['risk_metrics']['sharpe_ratio']:.2f}")
    print(f"   🏆 Win Rate: {result.result['risk_metrics']['win_rate']:.1%}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_backtest_analyzer_return_metrics():
    """Test return metrics calculation"""
    print("\n🧪 Test 7: backtest_analyzer - Return Metrics")

    np.random.seed(42)
    returns = np.array([0.05, -0.03, 0.08, 0.02, -0.01])

    backtest_results = pd.DataFrame({
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "benchmark_return": 0.10,
        "include_drawdown_analysis": False,
        "include_trade_stats": False
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    return_metrics = result.result["return_metrics"]

    assert "total_return" in return_metrics
    assert "best_trade" in return_metrics
    assert "worst_trade" in return_metrics
    assert "avg_return" in return_metrics

    # Verify calculations
    expected_total = returns.sum()
    assert abs(return_metrics["total_return"] - expected_total) < 0.0001

    print(f"   ✅ Return metrics calculated correctly")
    print(f"   📊 Total Return: {return_metrics['total_return']:.4f}")
    print(f"   📈 Best Trade: {return_metrics['best_trade']:.4f}")
    print(f"   📉 Worst Trade: {return_metrics['worst_trade']:.4f}")

    return True


def test_backtest_analyzer_risk_metrics():
    """Test risk metrics calculation"""
    print("\n🧪 Test 8: backtest_analyzer - Risk Metrics")

    np.random.seed(42)
    returns = np.array([0.05, -0.03, 0.08, 0.02, -0.01])

    backtest_results = pd.DataFrame({
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "risk_free_rate": 0.02
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    risk_metrics = result.result["risk_metrics"]

    assert "win_rate" in risk_metrics
    assert "sharpe_ratio" in risk_metrics
    assert "sortino_ratio" in risk_metrics

    # Verify win rate
    expected_win_rate = 0.6  # 3 winners out of 5
    assert abs(risk_metrics["win_rate"] - expected_win_rate) < 0.0001

    print(f"   ✅ Risk metrics calculated correctly")
    print(f"   🎯 Win Rate: {risk_metrics['win_rate']:.2%}")
    print(f"   📊 Sharpe Ratio: {risk_metrics['sharpe_ratio']:.2f}")
    print(f"   📈 Sortino Ratio: {risk_metrics['sortino_ratio']:.2f}")

    return True


def test_backtest_analyzer_drawdown_analysis():
    """Test drawdown analysis"""
    print("\n🧪 Test 9: backtest_analyzer - Drawdown Analysis")

    # Create returns with clear drawdown pattern
    returns = np.array([0.05, 0.03, -0.10, -0.05, 0.02, 0.04])

    backtest_results = pd.DataFrame({
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "include_drawdown_analysis": True,
        "include_trade_stats": False
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    dd_analysis = result.result["drawdown_analysis"]

    assert "max_drawdown" in dd_analysis
    assert "avg_drawdown" in dd_analysis
    assert dd_analysis["max_drawdown"] < 0  # Should be negative

    print(f"   ✅ Drawdown analysis completed")
    print(f"   📉 Max Drawdown: {dd_analysis['max_drawdown']:.2%}")
    print(f"   📊 Avg Drawdown: {dd_analysis['avg_drawdown']:.2%}")

    return True


def test_backtest_analyzer_trade_stats():
    """Test trade statistics"""
    print("\n🧪 Test 10: backtest_analyzer - Trade Statistics")

    np.random.seed(42)
    returns = np.array([0.05, -0.03, 0.08, 0.02, -0.01, 0.06, -0.04])

    backtest_results = pd.DataFrame({
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "include_drawdown_analysis": False,
        "include_trade_stats": True
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    trade_stats = result.result["trade_statistics"]

    assert "total_trades" in trade_stats
    assert "winning_trades" in trade_stats
    assert "losing_trades" in trade_stats
    assert "profit_factor" in trade_stats

    print(f"   ✅ Trade statistics calculated")
    print(f"   🔢 Total Trades: {trade_stats['total_trades']}")
    print(f"   🏆 Winning Trades: {trade_stats['winning_trades']}")
    print(f"   📉 Losing Trades: {trade_stats['losing_trades']}")
    print(f"   💰 Profit Factor: {trade_stats['profit_factor']:.2f}")

    return True


def test_backtest_analyzer_validation():
    """Test input validation"""
    print("\n🧪 Test 11: backtest_analyzer - Validation")

    # Missing backtest_results
    input_data = {}

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty DataFrame
    input_data = {
        "backtest_results": pd.DataFrame()
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INSUFFICIENT_DATA"

    # Missing required columns
    input_data = {
        "backtest_results": pd.DataFrame({'ticker': ['AAPL', 'TSLA']})
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_COLUMNS"

    print(f"   ✅ Input validation working correctly")

    return True


def test_backtest_analyzer_overall_score():
    """Test overall score calculation"""
    print("\n🧪 Test 12: backtest_analyzer - Overall Score")

    # Generate excellent returns
    np.random.seed(42)
    returns = np.random.normal(0.05, 0.05, 50)  # 5% avg return, low vol

    backtest_results = pd.DataFrame({
        'return': returns
    })

    input_data = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "include_drawdown_analysis": True,
        "include_trade_stats": True
    }

    result = backtest_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    overall_score = result.result["overall_score"]

    assert 0 <= overall_score <= 100

    print(f"   ✅ Overall score calculated")
    print(f"   ⭐ Overall Score: {overall_score}/100")
    print(f"   📝 Summary: {result.result['analysis_summary']}")

    return True


def test_performance_backtest_tools():
    """Performance test: Run both tools and measure execution time"""
    print("\n🚀 Test 13: Performance Test - Backtest Tools")

    times = []

    # Test 1: Backtest Generator
    backtest_config = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000
    }

    start = datetime.now()
    backtest_generator({
        "scanner_code": SAMPLE_SCANNER,
        "backtest_config": backtest_config,
        "include_comments": True,
        "include_visualization": True
    })
    times.append(("backtest_generator", (datetime.now() - start).total_seconds()))

    # Test 2: Backtest Analyzer
    np.random.seed(42)
    backtest_results = pd.DataFrame({
        'return': np.random.normal(0.02, 0.08, 50)
    })

    start = datetime.now()
    backtest_analyzer({
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "include_drawdown_analysis": True,
        "include_trade_stats": True
    })
    times.append(("backtest_analyzer", (datetime.now() - start).total_seconds()))

    print("\n   ⚡ Performance Results:")
    total_time = 0
    for name, time_taken in times:
        print(f"      • {name}: {time_taken:.4f}s")
        total_time += time_taken

    print(f"\n   📊 Total execution time: {total_time:.4f}s")
    print(f"   📈 Average: {total_time / len(times):.4f}s")

    # Performance targets: <0.5s for backtest_generator, <1s for backtest_analyzer
    assert times[0][1] < 0.5, "backtest_generator too slow"
    assert times[1][1] < 1.0, "backtest_analyzer too slow"

    print(f"   ✅ All tools within performance targets")

    return True


def run_all_tests():
    """Run all tests and report results"""

    print("=" * 70)
    print("🧪 BACKTEST TOOLS TEST SUITE")
    print("=" * 70)

    tests = [
        ("Backtest Generator - Basic Generation", test_backtest_generator_basic),
        ("Backtest Generator - With Visualization", test_backtest_generator_with_visualization),
        ("Backtest Generator - No Comments", test_backtest_generator_without_comments),
        ("Backtest Generator - Parameter Extraction", test_backtest_generator_parameter_extraction),
        ("Backtest Generator - Validation", test_backtest_generator_validation),
        ("Backtest Analyzer - Basic Analysis", test_backtest_analyzer_basic),
        ("Backtest Analyzer - Return Metrics", test_backtest_analyzer_return_metrics),
        ("Backtest Analyzer - Risk Metrics", test_backtest_analyzer_risk_metrics),
        ("Backtest Analyzer - Drawdown Analysis", test_backtest_analyzer_drawdown_analysis),
        ("Backtest Analyzer - Trade Stats", test_backtest_analyzer_trade_stats),
        ("Backtest Analyzer - Validation", test_backtest_analyzer_validation),
        ("Backtest Analyzer - Overall Score", test_backtest_analyzer_overall_score),
        ("Performance Test", test_performance_backtest_tools),
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
