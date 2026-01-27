"""
Test Suite for Market Analysis Tools

Tests for:
1. indicator_calculator - Calculate proprietary indicators
2. market_structure_analyzer - Detect pivots, trends, S/R levels
3. daily_context_detector - Detect daily market molds
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Import tools to test
from tools.indicator_calculator import indicator_calculator
from tools.market_structure_analyzer import market_structure_analyzer
from tools.daily_context_detector import daily_context_detector
from tools.tool_types import ToolStatus


def generate_sample_ohlcv(num_bars=100, trend='uptrend') -> pd.DataFrame:
    """Generate sample OHLCV data for testing"""

    dates = pd.date_range(start="2024-01-01", periods=num_bars, freq="D")
    np.random.seed(42)

    if trend == 'uptrend':
        # Generate uptrend data
        close_prices = np.linspace(100, 150, num_bars)
    elif trend == 'downtrend':
        # Generate downtrend data
        close_prices = np.linspace(150, 100, num_bars)
    else:
        # Sideways
        close_prices = np.random.uniform(140, 160, num_bars)

    # Add noise
    high_noise = np.random.uniform(0, 3, num_bars)
    low_noise = np.random.uniform(-3, 0, num_bars)

    df = pd.DataFrame({
        'open': close_prices + np.random.uniform(-1, 1, num_bars),
        'high': close_prices + high_noise,
        'low': close_prices + low_noise,
        'close': close_prices,
        'volume': np.random.randint(1000000, 5000000, num_bars)
    }, index=dates)

    return df


def test_indicator_calculator_72_89_cloud():
    """Test 72/89 EMA Cloud calculation"""
    print("\n🧪 Test 1: indicator_calculator - 72/89 Cloud")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud"],
        "lookback_period": 50
    }

    result = indicator_calculator(input_data)

    assert result.status == ToolStatus.SUCCESS, f"Expected SUCCESS, got {result.status}"
    assert "indicators" in result.result, "Missing 'indicators' in result"
    assert "72_89_cloud" in result.result["indicators"], "Missing 72_89_cloud data"

    cloud_data = result.result["indicators"]["72_89_cloud"]
    assert "upper" in cloud_data, "Missing upper band"
    assert "lower" in cloud_data, "Missing lower band"
    assert "current_position" in cloud_data, "Missing position"

    print(f"   ✅ 72/89 Cloud calculated successfully")
    print(f"   📊 Position: {cloud_data['current_position']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_indicator_calculator_9_20_cloud():
    """Test 9/20 EMA Cloud calculation"""
    print("\n🧪 Test 2: indicator_calculator - 9/20 Cloud")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "TSLA",
        "df": df,
        "indicators": ["9_20_cloud"],
        "lookback_period": 50
    }

    result = indicator_calculator(input_data)

    assert result.status == ToolStatus.SUCCESS, f"Expected SUCCESS, got {result.status}"
    assert "9_20_cloud" in result.result["indicators"], "Missing 9_20_cloud data"

    cloud_data = result.result["indicators"]["9_20_cloud"]
    assert "current_position" in cloud_data, "Missing position"

    print(f"   ✅ 9/20 Cloud calculated successfully")
    print(f"   📊 Position: {cloud_data['current_position']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_indicator_calculator_deviation_bands():
    """Test Deviation Bands calculation"""
    print("\n🧪 Test 3: indicator_calculator - Deviation Bands")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "NVDA",
        "df": df,
        "indicators": ["deviation_bands"],
        "lookback_period": 50
    }

    result = indicator_calculator(input_data)

    assert result.status == ToolStatus.SUCCESS, f"Expected SUCCESS, got {result.status}"
    assert "deviation_bands" in result.result["indicators"], "Missing deviation_bands data"

    bands = result.result["indicators"]["deviation_bands"]
    assert "upper" in bands, "Missing upper band"
    assert "lower" in bands, "Missing lower band"
    assert "mean" in bands, "Missing mean"

    print(f"   ✅ Deviation Bands calculated successfully")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_indicator_calculator_all():
    """Test calculating all indicators at once"""
    print("\n🧪 Test 4: indicator_calculator - All Indicators")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"],
        "lookback_period": 50
    }

    result = indicator_calculator(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert len(result.result["indicators"]) == 3

    print(f"   ✅ All 3 indicators calculated successfully")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_indicator_calculator_validation():
    """Test input validation"""
    print("\n🧪 Test 5: indicator_calculator - Validation")

    # Missing required field
    input_data = {
        "ticker": "AAPL",
        "df": generate_sample_ohlcv(100)
        # Missing "indicators"
    }

    result = indicator_calculator(input_data)

    assert result.status == ToolStatus.ERROR, "Expected ERROR for missing indicators"
    assert result.error["code"] == "MISSING_PARAMETER"

    print(f"   ✅ Validation working correctly")

    return True


def test_market_structure_analyzer_trend():
    """Test trend analysis"""
    print("\n🧪 Test 6: market_structure_analyzer - Trend Analysis")

    df = generate_sample_ohlcv(100, trend='uptrend')

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "lookback_period": 20,
        "trend_method": "hh_hl"
    }

    result = market_structure_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "trend" in result.result

    trend = result.result["trend"]
    assert "direction" in trend
    assert "strength" in trend
    assert "higher_highs" in trend
    assert "higher_lows" in trend

    print(f"   ✅ Trend analyzed successfully")
    print(f"   📊 Direction: {trend['direction']}")
    print(f"   💪 Strength: {trend['strength']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_market_structure_analyzer_pivots():
    """Test pivot detection"""
    print("\n🧪 Test 7: market_structure_analyzer - Pivot Detection")

    df = generate_sample_ohlcv(100, trend='uptrend')

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "lookback_period": 10,
        "min_swing_strength": 0.02
    }

    result = market_structure_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "pivot_highs" in result.result
    assert "pivot_lows" in result.result

    pivot_highs = result.result["pivot_highs"]
    pivot_lows = result.result["pivot_lows"]

    print(f"   ✅ Pivots detected successfully")
    print(f"   🔺 Pivot Highs: {len(pivot_highs)}")
    print(f"   🔻 Pivot Lows: {len(pivot_lows)}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_market_structure_analyzer_support_resistance():
    """Test support and resistance level calculation"""
    print("\n🧪 Test 8: market_structure_analyzer - Support/Resistance")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "support_levels": 3,
        "resistance_levels": 3
    }

    result = market_structure_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "support_levels" in result.result
    assert "resistance_levels" in result.result

    support = result.result["support_levels"]
    resistance = result.result["resistance_levels"]

    print(f"   ✅ Support/Resistance calculated successfully")
    print(f"   📈 Support Levels: {len(support)}")
    print(f"   📉 Resistance Levels: {len(resistance)}")

    if support:
        print(f"   💪 Nearest Support: ${support[0]['price']:.2f} (strength: {support[0]['strength']})")
    if resistance:
        print(f"   🛑 Nearest Resistance: ${resistance[0]['price']:.2f} (strength: {resistance[0]['strength']})")

    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_market_structure_analyzer_current_position():
    """Test current position analysis"""
    print("\n🧪 Test 9: market_structure_analyzer - Current Position")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df
    }

    result = market_structure_analyzer(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "current_position" in result.result

    position = result.result["current_position"]
    assert "near_level" in position
    assert "distance_to_support_pct" in position
    assert "distance_to_resistance_pct" in position

    print(f"   ✅ Current position analyzed successfully")
    print(f"   📍 Position: {position['near_level']}")
    print(f"   📊 Distance to Support: {position['distance_to_support_pct']}%")
    print(f"   📊 Distance to Resistance: {position['distance_to_resistance_pct']}%")

    return True


def test_daily_context_detector_backside_b():
    """Test Backside B pattern detection"""
    print("\n🧪 Test 10: daily_context_detector - Backside B")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "market_date": "2024-01-26",
        "mold_types": ["BACKSIDE_B"],
        "gap_threshold": 0.01,
        "atr_period": 14
    }

    result = daily_context_detector(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "daily_mold" in result.result
    assert "gap_analysis" in result.result
    assert "opening_range" in result.result

    mold = result.result["daily_mold"]
    gap = result.result["gap_analysis"]

    print(f"   ✅ Daily context detected successfully")
    print(f"   🎯 Mold Type: {mold['type']}")
    print(f"   📊 Gap: {gap['gap_type']} ({gap['gap_size_atr']} ATR)")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_daily_context_detector_multiple_molds():
    """Test detecting multiple mold types"""
    print("\n🧪 Test 11: daily_context_detector - Multiple Molds")

    df = generate_sample_ohlcv(100)

    input_data = {
        "ticker": "AAPL",
        "df": df,
        "market_date": "2024-01-26",
        "mold_types": ["BACKSIDE_B", "MDR", "D2", "FBO", "T30"],
        "confidence_threshold": 0.7
    }

    result = daily_context_detector(input_data)

    assert result.status == ToolStatus.SUCCESS
    assert "daily_mold" in result.result
    assert "alternative_molds" in result.result
    assert "recommended_setup" in result.result

    print(f"   ✅ Multiple molds detected successfully")
    print(f"   🎯 Primary Mold: {result.result['daily_mold']['type']}")
    print(f"   🔀 Alternatives: {len(result.result['alternative_molds'])}")
    print(f"   💡 Recommended Setup: {result.result['recommended_setup']['name']}")
    print(f"   ⚡ Execution time: {result.execution_time:.4f}s")

    return True


def test_daily_context_detector_validation():
    """Test input validation"""
    print("\n🧪 Test 12: daily_context_detector - Validation")

    # Missing market_date
    input_data = {
        "ticker": "AAPL",
        "df": generate_sample_ohlcv(100)
        # Missing "market_date"
    }

    result = daily_context_detector(input_data)

    assert result.status == ToolStatus.ERROR
    assert result.error["code"] == "MISSING_PARAMETER"

    print(f"   ✅ Validation working correctly")

    return True


def test_performance_all_tools():
    """Performance test: Run all tools and measure execution time"""
    print("\n🚀 Test 13: Performance Test - All Tools")

    df = generate_sample_ohlcv(100)

    times = []

    # Test 1: Indicator Calculator (all 3 indicators)
    start = datetime.now()
    indicator_calculator({
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"]
    })
    times.append(("indicator_calculator", (datetime.now() - start).total_seconds()))

    # Test 2: Market Structure Analyzer
    start = datetime.now()
    market_structure_analyzer({
        "ticker": "AAPL",
        "df": df,
        "support_levels": 3,
        "resistance_levels": 3
    })
    times.append(("market_structure_analyzer", (datetime.now() - start).total_seconds()))

    # Test 3: Daily Context Detector
    start = datetime.now()
    daily_context_detector({
        "ticker": "AAPL",
        "df": df,
        "market_date": "2024-01-26",
        "mold_types": ["BACKSIDE_B", "MDR", "D2", "FBO", "T30"]
    })
    times.append(("daily_context_detector", (datetime.now() - start).total_seconds()))

    print("\n   ⚡ Performance Results:")
    total_time = 0
    for name, time_taken in times:
        print(f"      • {name}: {time_taken:.4f}s")
        total_time += time_taken

    print(f"\n   📊 Total execution time: {total_time:.4f}s")
    print(f"   📈 Average: {total_time / len(times):.4f}s")

    # Performance targets: <0.5s for indicator and context, <1s for structure
    assert times[0][1] < 0.5, "indicator_calculator too slow"
    assert times[1][1] < 1.0, "market_structure_analyzer too slow"
    assert times[2][1] < 0.5, "daily_context_detector too slow"

    print(f"   ✅ All tools within performance targets")

    return True


def run_all_tests():
    """Run all tests and report results"""

    print("=" * 70)
    print("🧪 MARKET ANALYSIS TOOLS TEST SUITE")
    print("=" * 70)

    tests = [
        ("Indicator Calculator - 72/89 Cloud", test_indicator_calculator_72_89_cloud),
        ("Indicator Calculator - 9/20 Cloud", test_indicator_calculator_9_20_cloud),
        ("Indicator Calculator - Deviation Bands", test_indicator_calculator_deviation_bands),
        ("Indicator Calculator - All Indicators", test_indicator_calculator_all),
        ("Indicator Calculator - Validation", test_indicator_calculator_validation),
        ("Market Structure Analyzer - Trend", test_market_structure_analyzer_trend),
        ("Market Structure Analyzer - Pivots", test_market_structure_analyzer_pivots),
        ("Market Structure Analyzer - Support/Resistance", test_market_structure_analyzer_support_resistance),
        ("Market Structure Analyzer - Current Position", test_market_structure_analyzer_current_position),
        ("Daily Context Detector - Backside B", test_daily_context_detector_backside_b),
        ("Daily Context Detector - Multiple Molds", test_daily_context_detector_multiple_molds),
        ("Daily Context Detector - Validation", test_daily_context_detector_validation),
        ("Performance Test", test_performance_all_tools),
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
