"""
Test Suite for Validation Tools

Tests for:
1. a_plus_analyzer - Validate scanners against A+ examples
2. quick_backtester - Fast 30-day backtest validation
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tools to test
from tools.a_plus_analyzer import a_plus_analyzer
from tools.quick_backtester import quick_backtester
from tools.tool_types import ToolStatus


# Sample scanner code for testing
SAMPLE_SCANNER_BACKSIDE_B = """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    # Backside B setup detection
    gap = df['open'] - df['close'].shift(1)
    atr = calculate_atr(df, 14)
    gap_over_atr = gap / atr

    # Check for gap up into resistance
    ema72 = df['close'].ewm(span=72).mean()
    ema89 = df['close'].ewm(span=89).mean()

    if gap_over_atr > 0.8 and df['close'].iloc[-1] > ema72.iloc[-1]:
        return {
            'setup_type': 'BACKSIDE_B',
            'entry_price': df['close'].iloc[-1]
        }

    return None
"""

SAMPLE_SCANNER_MULTI_SETUP = """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    # Backside B
    gap = df['open'] - df['close'].shift(1)
    atr = calculate_atr(df, 14)
    gap_over_atr = gap / atr

    # D2 continuation
    ema9 = df['close'].ewm(span=9).mean()
    ema20 = df['close'].ewm(span=20).mean()

    # Volume filter
    volume_ma = df['volume'].rolling(20).mean()

    if gap_over_atr > 0.8:
        return {'setup_type': 'BACKSIDE_B'}
    elif df['close'].iloc[-1] > ema9.iloc[-1]:
        return {'setup_type': 'D2'}
    elif df['volume'].iloc[-1] > volume_ma.iloc[-1] * 1.5:
        return {'setup_type': 'FBO'}

    return None
"""


def test_a_plus_analyzer_basic():
    """Test basic A+ analysis"""
    print("\n🧪 Test 1: a_plus_analyzer - Basic Analysis")

    a_plus_examples = [
        {
            "ticker": "AAPL",
            "date": "2024-01-15",
            "setup_type": "BACKSIDE_B",
            "entry_price": 150.25
        },
        {
            "ticker": "TSLA",
            "date": "2024-01-16",
            "setup_type": "BACKSIDE_B",
            "entry_price": 220.50
        }
    ]

    input_data = {
        "scanner_code": SAMPLE_SCANNER_BACKSIDE_B,
        "a_plus_examples": a_plus_examples,
        "strict_mode": False,
        "return_details": True
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "validation_passed" in result.result
    assert "catch_rate" in result.result
    assert "scanner_capabilities" in result.result

    print(f"   ✅ A+ analysis completed successfully")
    print(f"   📊 Validation Passed: {result.result['validation_passed']}")
    print(f"   🎯 Catch Rate: {result.result['catch_rate']:.1%}")
    print(f"   📈 Capabilities: {result.result['scanner_capabilities']['total_capabilities']}/4")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_a_plus_analyzer_multi_setup():
    """Test with multi-setup scanner"""
    print("\n🧪 Test 2: a_plus_analyzer - Multi-Setup Scanner")

    a_plus_examples = [
        {"ticker": "AAPL", "date": "2024-01-15", "setup_type": "BACKSIDE_B", "entry_price": 150.25},
        {"ticker": "TSLA", "date": "2024-01-16", "setup_type": "D2", "entry_price": 220.50},
        {"ticker": "NVDA", "date": "2024-01-17", "setup_type": "FBO", "entry_price": 580.75}
    ]

    input_data = {
        "scanner_code": SAMPLE_SCANNER_MULTI_SETUP,
        "a_plus_examples": a_plus_examples,
        "strict_mode": False,
        "return_details": True
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert result.result["total_examples"] == 3

    capabilities = result.result["scanner_capabilities"]
    setup_types = capabilities["setup_types_detected"]

    print(f"   ✅ Multi-setup analysis completed")
    print(f"   📊 Detected Setups: {setup_types}")
    print(f"   🎯 Catch Rate: {result.result['catch_rate']:.1%}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_a_plus_analyzer_strict_mode():
    """Test strict mode validation"""
    print("\n🧪 Test 3: a_plus_analyzer - Strict Mode")

    a_plus_examples = [
        {"ticker": "AAPL", "date": "2024-01-15", "setup_type": "BACKSIDE_B", "entry_price": 150.25},
        {"ticker": "TSLA", "date": "2024-01-16", "setup_type": "D2", "entry_price": 220.50}
    ]

    input_data = {
        "scanner_code": SAMPLE_SCANNER_BACKSIDE_B,  # Only catches BACKSIDE_B
        "a_plus_examples": a_plus_examples,
        "strict_mode": True,  # Require 100% catch rate
        "return_details": True
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "validation_passed" in result.result
    # Should fail strict mode because it won't catch D2 setup

    print(f"   ✅ Strict mode validation completed")
    print(f"   📊 Validation Passed (strict): {result.result['validation_passed']}")
    print(f"   🎯 Caught: {result.result['caught_examples']}/{result.result['total_examples']}")

    return True


def test_a_plus_analyzer_validation():
    """Test input validation"""
    print("\n🧪 Test 4: a_plus_analyzer - Validation")

    # Missing scanner_code
    input_data = {
        "a_plus_examples": []
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty a_plus_examples
    input_data = {
        "scanner_code": SAMPLE_SCANNER_BACKSIDE_B,
        "a_plus_examples": []
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INVALID_INPUT"

    print(f"   ✅ Input validation working correctly")

    return True


def test_a_plus_analyzer_capabilities():
    """Test capability detection"""
    print("\n🧪 Test 5: a_plus_analyzer - Capability Detection")

    scanner_with_features = """
    # Scanner with multiple features
    gap = df['open'] - df['close'].shift(1)
    atr = calculate_atr(df, 14)
    volume_ma = df['volume'].rolling(20).mean()
    ema_cloud_72_89 = df['close'].ewm(span=72).mean()

    rsi = calculate_rsi(df, 14)
    macd = calculate_macd(df)
    """

    a_plus_examples = [
        {"ticker": "AAPL", "date": "2024-01-15", "setup_type": "BACKSIDE_B", "entry_price": 150.25}
    ]

    input_data = {
        "scanner_code": scanner_with_features,
        "a_plus_examples": a_plus_examples
    }

    result = a_plus_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    capabilities = result.result["scanner_capabilities"]

    assert capabilities["has_gap_detection"] == True
    assert capabilities["has_atr_filter"] == True
    assert capabilities["has_volume_filter"] == True
    assert capabilities["has_ema_cloud"] == True
    assert capabilities["has_rsi_indicator"] == True
    assert capabilities["has_macd_indicator"] == True

    print(f"   ✅ Capability detection working correctly")
    print(f"   📊 Capability Score: {capabilities['capability_score']:.2%}")

    return True


def test_quick_backtester_basic():
    """Test basic backtest"""
    print("\n🧪 Test 6: quick_backtester - Basic Backtest")

    # Generate sample scanner results
    np.random.seed(42)
    num_trades = 25

    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]
    entry_prices = np.random.uniform(100, 200, num_trades)
    returns = np.random.normal(0.01, 0.05, num_trades)
    exit_prices = entry_prices * (1 + returns)

    scanner_results = pd.DataFrame({
        'date': dates[:num_trades],
        'ticker': np.random.choice(['AAPL', 'TSLA', 'NVDA'], num_trades),
        'entry_price': entry_prices,
        'exit_price': exit_prices
    })

    input_data = {
        "scanner_results": scanner_results,
        "entry_price_col": "entry_price",
        "exit_price_col": "exit_price",
        "date_col": "date",
        "return_trades": True
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "total_trades" in result.result
    assert "win_rate" in result.result
    assert "total_return" in result.result
    assert "sharpe_ratio" in result.result

    print(f"   ✅ Quick backtest completed successfully")
    print(f"   📊 Total Trades: {result.result['total_trades']}")
    print(f"   🎯 Win Rate: {result.result['win_rate']:.1%}")
    print(f"   📈 Total Return: {result.result['total_return']:.2%}")
    print(f"   📊 Sharpe Ratio: {result.result['sharpe_ratio']:.2f}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_quick_backtester_trade_distribution():
    """Test trade distribution analysis"""
    print("\n🧪 Test 7: quick_backtester - Trade Distribution")

    # Generate results with known distribution
    scanner_results = pd.DataFrame({
        'date': [datetime.now() - timedelta(days=i) for i in range(10, 0, -1)],
        'entry_price': [100] * 10,
        'exit_price': [
            110,  # +10% (large gain)
            103,  # +3% (small gain)
            95,   # -5% (small loss)
            90,   # -10% (large loss)
            104,  # +4% (small gain)
            92,   # -8% (large loss)
            102,  # +2% (small gain)
            97,   # -3% (small loss)
            108,  # +8% (small gain)
            94    # -6% (large loss)
        ]
    })

    input_data = {
        "scanner_results": scanner_results,
        "return_trades": True
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.SUCCESS
    trade_analysis = result.result["trade_analysis"]

    assert "return_distribution" in trade_analysis
    assert "avg_winner" in trade_analysis
    assert "avg_loser" in trade_analysis
    assert "profit_factor" in trade_analysis

    distribution = trade_analysis["return_distribution"]
    assert distribution["large_gains"] == 2  # 2 trades >5% gain (10% and 8%)
    assert distribution["large_losses"] == 3  # 3 losses >5%

    print(f"   ✅ Trade distribution analysis completed")
    print(f"   📊 Large Gains: {distribution['large_gains']}")
    print(f"   📊 Large Losses: {distribution['large_losses']}")
    print(f"   💰 Avg Winner: {trade_analysis['avg_winner']:.2%}")
    print(f"   📉 Avg Loser: {trade_analysis['avg_loser']:.2%}")
    print(f"   📊 Profit Factor: {trade_analysis['profit_factor']:.2f}")

    return True


def test_quick_backtester_trades_detail():
    """Test individual trade details"""
    print("\n🧪 Test 8: quick_backtester - Trade Details")

    scanner_results = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=5),
        'ticker': ['AAPL', 'TSLA', 'NVDA', 'AMD', 'MSFT'],
        'entry_price': [100, 200, 150, 80, 300],
        'exit_price': [105, 195, 160, 75, 310]  # 3 wins, 2 losses
    })

    input_data = {
        "scanner_results": scanner_results,
        "return_trades": True
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.SUCCESS
    trades_detail = result.result["trades_detail"]

    assert len(trades_detail) == 5

    # Check first trade
    first_trade = trades_detail[0]
    assert "date" in first_trade
    assert "entry_price" in first_trade
    assert "exit_price" in first_trade
    assert "return" in first_trade
    assert "result" in first_trade

    print(f"   ✅ Trade details prepared correctly")
    print(f"   📊 Total Trades: {len(trades_detail)}")
    print(f"   📈 First Trade: {first_trade['result']} ({first_trade['return']:.2%})")

    return True


def test_quick_backtester_validation():
    """Test input validation"""
    print("\n🧪 Test 9: quick_backtester - Validation")

    # Missing scanner_results
    input_data = {}

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    # Empty DataFrame
    input_data = {
        "scanner_results": pd.DataFrame()
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "INSUFFICIENT_DATA"

    # Missing required columns
    input_data = {
        "scanner_results": pd.DataFrame({'date': [1, 2, 3]})  # Missing entry/exit cols
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_COLUMNS"

    print(f"   ✅ Input validation working correctly")

    return True


def test_quick_backtester_benchmark_comparison():
    """Test benchmark comparison"""
    print("\n🧪 Test 10: quick_backtester - Benchmark Comparison")

    # Generate profitable results
    scanner_results = pd.DataFrame({
        'date': [datetime.now() - timedelta(days=i) for i in range(10, 0, -1)],
        'entry_price': [100] * 10,
        'exit_price': [105] * 10  # 5% gain each trade
    })

    benchmark_return = 0.02  # 2% benchmark

    input_data = {
        "scanner_results": scanner_results,
        "benchmark_return": benchmark_return
    }

    result = quick_backtester(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert result.result["benchmark_return"] == benchmark_return
    assert result.result["vs_benchmark"] > 0  # Should beat benchmark

    print(f"   ✅ Benchmark comparison completed")
    print(f"   📊 Total Return: {result.result['total_return']:.2%}")
    print(f"   📊 Benchmark: {benchmark_return:.2%}")
    print(f"   📈 vs Benchmark: {result.result['vs_benchmark']:.2%}")

    return True


def test_performance_validation_tools():
    """Performance test: Run both tools and measure execution time"""
    print("\n🚀 Test 11: Performance Test - Validation Tools")

    times = []

    # Test 1: A+ Analyzer
    a_plus_examples = [
        {"ticker": "AAPL", "date": "2024-01-15", "setup_type": "BACKSIDE_B", "entry_price": 150.25},
        {"ticker": "TSLA", "date": "2024-01-16", "setup_type": "D2", "entry_price": 220.50},
        {"ticker": "NVDA", "date": "2024-01-17", "setup_type": "FBO", "entry_price": 580.75}
    ]

    start = datetime.now()
    a_plus_analyzer({
        "scanner_code": SAMPLE_SCANNER_MULTI_SETUP,
        "a_plus_examples": a_plus_examples,
        "return_details": True
    })
    times.append(("a_plus_analyzer", (datetime.now() - start).total_seconds()))

    # Test 2: Quick Backtester
    num_trades = 25
    scanner_results = pd.DataFrame({
        'date': [datetime.now() - timedelta(days=i) for i in range(num_trades, 0, -1)],
        'entry_price': np.random.uniform(100, 200, num_trades),
        'exit_price': np.random.uniform(100, 200, num_trades)
    })

    start = datetime.now()
    quick_backtester({
        "scanner_results": scanner_results,
        "return_trades": True
    })
    times.append(("quick_backtester", (datetime.now() - start).total_seconds()))

    print("\n   ⚡ Performance Results:")
    total_time = 0
    for name, time_taken in times:
        print(f"      • {name}: {time_taken:.4f}s")
        total_time += time_taken

    print(f"\n   📊 Total execution time: {total_time:.4f}s")
    print(f"   📈 Average: {total_time / len(times):.4f}s")

    # Performance targets: <1s for a_plus_analyzer, <2s for quick_backtester
    assert times[0][1] < 1.0, "a_plus_analyzer too slow"
    assert times[1][1] < 2.0, "quick_backtester too slow"

    print(f"   ✅ All tools within performance targets")

    return True


def run_all_tests():
    """Run all tests and report results"""

    print("=" * 70)
    print("🧪 VALIDATION TOOLS TEST SUITE")
    print("=" * 70)

    tests = [
        ("A+ Analyzer - Basic Analysis", test_a_plus_analyzer_basic),
        ("A+ Analyzer - Multi-Setup Scanner", test_a_plus_analyzer_multi_setup),
        ("A+ Analyzer - Strict Mode", test_a_plus_analyzer_strict_mode),
        ("A+ Analyzer - Validation", test_a_plus_analyzer_validation),
        ("A+ Analyzer - Capability Detection", test_a_plus_analyzer_capabilities),
        ("Quick Backtester - Basic Backtest", test_quick_backtester_basic),
        ("Quick Backtester - Trade Distribution", test_quick_backtester_trade_distribution),
        ("Quick Backtester - Trade Details", test_quick_backtester_trades_detail),
        ("Quick Backtester - Validation", test_quick_backtester_validation),
        ("Quick Backtester - Benchmark Comparison", test_quick_backtester_benchmark_comparison),
        ("Performance Test", test_performance_validation_tools),
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
