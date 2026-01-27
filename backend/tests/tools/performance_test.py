"""
Realistic Performance Tests for Core Scanner Tools

Tests with ACTUAL V31 scanner code (300+ lines) to get realistic timing measurements.
"""

import sys
import time
from pathlib import Path

# Add tools to path
backend_src = Path(__file__).parent.parent.parent / "src" / "tools"
sys.path.insert(0, str(backend_src))

from tool_types import ToolStatus
from v31_scanner_generator import v31_scanner_generator
from v31_validator import v31_validator


# REAL V31 SCANNER CODE (300+ lines) - Back to the Future Scanner
REAL_V31_SCANNER = """
# V31 Scanner: Back to the Future Setup
# Generated: 2024-01-26
# Description: Gap up continuation after red candle

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ====================
# PARAMETERS
# ====================
# gap_over_atr: range 0.8-1.5
gap_over_atr_min = 0.8
gap_over_atr_max = 1.5
gap_over_atr_default = 1.0

# open_over_ema9: range 0.90-0.98
open_over_ema9_min = 0.90
open_over_ema9_max = 0.98
open_over_ema9_default = 0.92

# min_volume: range 500000-2000000
min_volume_min = 500000
min_volume_max = 2000000
min_volume_default = 1000000

# min_price: range 5-100
min_price_min = 5
min_price_max = 100
min_price_default = 10

# max_gap_percent: range 1.0-5.0
max_gap_percent_min = 1.0
max_gap_percent_max = 5.0
max_gap_percent_default = 3.0

# red_close_threshold: range 0.0-0.5
red_close_threshold_min = 0.0
red_close_threshold_max = 0.5
red_close_threshold_default = 0.2

# ====================
# STAGE 1: MARKET SCANNING
# ====================
def get_stage1_symbols():
    \"\"\"Fetch all symbols for market scanning\"\"\"
    # Return full market universe (12k+ tickers)
    # This is optimized via grouped API endpoints
    # Grouped by: price_range, volume_range, sector
    # Batch size: 1000 symbols per request
    return symbols  # Populated by backend

# ====================
# STAGE 2: PER-TICKER OPERATIONS
# ====================
def stage2_process_symbols(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Process each ticker independently through 3 stages:
    1. Data fetching
    2. Filtering & detection
    3. Signal generation

    Args:
        df: DataFrame with OHLCV data for single ticker

    Returns:
        DataFrame with signals or empty if no signals
    \"\"\"

    # Stage 2.1: Calculate indicators
    df = calculate_indicators(df)

    # Stage 2.2: Apply smart filters (quick rejections)
    if not passes_smart_filters(df):
        return pd.DataFrame()  # Empty = no signal

    # Stage 2.3: Detect setup
    signals_df = detect_setup(df)

    return signals_df


def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"Calculate required indicators for detection\"\"\"

    # ATR for volatility-adjusted parameters
    df['atr'] = calculate_atr(df, 14)
    df['atr_ratio'] = df['atr'] / df['close']

    # EMA9 for trend reference
    df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()

    # Gap detection
    df['prev_close'] = df['close'].shift(1)
    df['gap'] = df['open'] - df['prev_close']
    df['gap_over_atr'] = df['gap'] / df['atr']
    df['gap_percent'] = (df['gap'] / df['prev_close']) * 100

    # Open vs EMA9
    df['open_vs_ema9'] = df['open'] / df['ema9']

    # Red candle detection
    df['is_red'] = df['close'] < df['open']
    df['red_size'] = (df['open'] - df['close']) / df['open']
    df['body_size'] = abs(df['close'] - df['open']) / df['open']

    # Volume checks
    df['avg_volume_20'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['avg_volume_20']

    return df


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    \"\"\"Calculate Average True Range\"\"\"
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift(1))
    low_close = np.abs(df['low'] - df['close'].shift(1))

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    return true_range.rolling(window=period).mean()


def passes_smart_filters(df: pd.DataFrame) -> bool:
    \"\"\"
    Smart filters for quick rejection (Stage 2.2)
    Reject tickers that don't meet basic criteria

    Returns:
        True if ticker passes all filters, False otherwise
    \"\"\"

    latest = df.iloc[-1]

    # Filter 1: Minimum price
    if latest['close'] < min_price_default:
        return False

    # Filter 2: Minimum volume
    if latest['volume'] < min_volume_default:
        return False

    # Filter 3: Has gap
    if latest['gap_over_atr'] < gap_over_atr_min:
        return False

    # Filter 4: Gap not too large (avoid exhaustion gaps)
    if abs(latest['gap_percent']) > max_gap_percent_default:
        return False

    # Filter 5: Has sufficient data
    if len(df) < 50:
        return False

    return True


def detect_setup(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Detect Back to the Future setup (Stage 2.3)
    Gap up continuation after red candle

    Returns:
        DataFrame with signal details or empty if no signal
    \"\"\"

    # Get latest data
    latest = df.iloc[-1]
    previous = df.iloc[-2]

    # Condition 1: Gap up over ATR
    gap_condition = latest['gap_over_atr'] >= gap_over_atr_min

    # Condition 2: Open below EMA9 (gap into resistance)
    open_condition = latest['open_vs_ema9'] >= open_over_ema9_min

    # Condition 3: Previous day was red candle
    red_condition = previous['is_red']

    # Condition 4: Previous candle not too large (exhaustion check)
    exhaustion_check = previous['body_size'] < red_close_threshold_default

    # Condition 5: Current day showing continuation (green or small red)
    continuation = (not latest['is_red']) or (latest['body_size'] < 0.1)

    if all([gap_condition, open_condition, red_condition, exhaustion_check, continuation]):
        # Signal found!
        signal_df = pd.DataFrame([{
            'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
            'signal_time': df.index[-1],
            'entry_price': latest['close'],
            'gap_size': latest['gap_over_atr'],
            'gap_percent': latest['gap_percent'],
            'open_vs_ema9': latest['open_vs_ema9'],
            'previous_red': previous['body_size'],
            'volume_ratio': latest['volume_ratio'],
            'atr_ratio': latest['atr_ratio'],
            'confidence': calculate_confidence(latest, previous)
        }])

        return signal_df

    return pd.DataFrame()  # No signal


def calculate_confidence(latest: pd.Series, previous: pd.Series) -> float:
    \"\"\"Calculate signal confidence based on multiple factors\"\"\"

    confidence = 0.5  # Base confidence

    # Factor 1: Gap size (optimal range: 0.8-1.2)
    if 0.8 <= latest['gap_over_atr'] <= 1.2:
        confidence += 0.15

    # Factor 2: Open below EMA9 (stronger resistance)
    if latest['open_vs_ema9'] >= 0.95:
        confidence += 0.1

    # Factor 3: Previous red candle size (moderate is best)
    if 0.1 <= previous['body_size'] <= 0.3:
        confidence += 0.1

    # Factor 4: Volume confirmation
    if latest['volume_ratio'] >= 1.2:
        confidence += 0.1

    # Factor 5: Low ATR (stable environment)
    if latest['atr_ratio'] < 0.05:
        confidence += 0.05

    return min(confidence, 0.95)  # Cap at 0.95

# ====================
# STAGE 3: AGGREGATION
# ====================
def aggregate_signals(all_signals: list) -> pd.DataFrame:
    \"\"\"
    Aggregate signals from all tickers
    Apply final ranking and filtering

    Args:
        all_signals: List of DataFrames with signals

    Returns:
        Combined and ranked DataFrame
    \"\"\"

    if not all_signals:
        return pd.DataFrame()

    # Filter out empty DataFrames
    valid_signals = [s for s in all_signals if not s.empty]

    if not valid_signals:
        return pd.DataFrame()

    # Combine all signals
    combined = pd.concat(valid_signals, ignore_index=True)

    # Sort by confidence (descending)
    combined = combined.sort_values('confidence', ascending=False)

    # Add rank
    combined['rank'] = range(1, len(combined) + 1)

    return combined

# ====================
# ADDITIONAL HELPER FUNCTIONS
# ====================
def get_signal_metadata(df: pd.DataFrame) -> dict:
    \"\"\"Get metadata about detected signals\"\"\"

    return {
        'total_signals': len(df),
        'avg_confidence': df['confidence'].mean() if len(df) > 0 else 0,
        'avg_gap_size': df['gap_size'].mean() if len(df) > 0 else 0,
        'high_confidence_count': len(df[df['confidence'] >= 0.75]),
        'detection_time': datetime.now().isoformat()
    }


def validate_signal_quality(signal: pd.Series) -> bool:
    \"\"\"Validate signal meets minimum quality standards\"\"\"

    # Minimum confidence
    if signal['confidence'] < 0.6:
        return False

    # Gap size in reasonable range
    if signal['gap_size'] < 0.5 or signal['gap_size'] > 2.0:
        return False

    # Volume confirmation
    if signal['volume_ratio'] < 0.8:
        return False

    return True


# ====================
# PARAMETER OPTIMIZATION
# ====================
def optimize_parameters(df: pd.DataFrame) -> dict:
    \"\"\"Optimize parameters based on historical data\"\"\"

    # Calculate optimal values based on recent volatility
    recent_atr = df['atr'].tail(20).mean()
    recent_price = df['close'].tail(20).mean()

    optimized = {
        'gap_over_atr': recent_atr / recent_price * 1.2,
        'min_volume': int(df['volume'].tail(20).median()),
        'min_price': max(5, int(recent_price * 0.1))
    }

    return optimized


# ====================
# END OF SCANNER
# ====================
"""


def test_v31_validator_realistic():
    """Test v31_validator with REAL 300+ line scanner code"""

    print("=" * 80)
    print("TEST 1: v31_validator with REAL V31 Scanner Code (300+ lines)")
    print("=" * 80)

    start = time.time()
    result = v31_validator({
        "scanner_code": REAL_V31_SCANNER,
        "strict_mode": False,
        "return_fixes": True
    })
    elapsed = time.time() - start

    print(f"\n⏱️  Execution Time: {elapsed:.3f} seconds")
    print(f"✅ Status: {result.status}")
    print(f"📊 Compliance Score: {result.result['compliance_score']}")
    print(f"📋 Total Violations: {result.result['total_violations']}")
    print(f"🔴 Critical: {result.result['critical_violations']}")
    print(f"🟡 Major: {result.result['major_violations']}")
    print(f"🟢 Minor: {result.result['minor_violations']}")

    # Show pillar breakdown
    print("\n📊 Pillar Breakdown:")
    for pillar_name, pillar_result in result.result['pillar_results'].items():
        print(f"  {pillar_name}:")
        print(f"    Compliant: {pillar_result['compliant']}")
        print(f"    Score: {pillar_result['score']:.2f}")
        print(f"    Violations: {len(pillar_result['violations'])}")

    return elapsed


def test_v31_generator_with_validation():
    """Test v31_scanner_generator WITH validation enabled"""

    print("\n" + "=" * 80)
    print("TEST 2: v31_scanner_generator WITH Validation (Realistic)")
    print("=" * 80)

    start = time.time()
    result = v31_scanner_generator({
        "description": "Back to the Future scanner - gap up continuation after red candle with EMA9 resistance",
        "parameters": {
            "gap_over_atr": {"min": 0.8, "max": 1.5, "default": 1.0},
            "open_over_ema9": {"min": 0.90, "max": 0.98, "default": 0.92}
        },
        "include_comments": True,
        "include_validation": True,  # ENABLE VALIDATION
        "output_format": "python"
    })
    elapsed = time.time() - start

    print(f"\n⏱️  Execution Time: {elapsed:.3f} seconds")
    print(f"✅ Status: {result.status}")
    print(f"📏 Code Length: {len(result.result['scanner_code'])} characters")
    print(f"📏 Lines: {len(result.result['scanner_code'].split(chr(10)))} lines")
    print(f"✅ V31 Validated: {result.result['v31_validated']}")
    print(f"📊 Compliance Score: {result.result['validation_report']['compliance_score'] if result.result['validation_report'] else 'N/A'}")
    print(f"⚠️  Warnings: {len(result.result['warnings'])}")

    if result.result['warnings']:
        print("\n⚠️  Warnings:")
        for warning in result.result['warnings']:
            print(f"  - {warning}")

    return elapsed


def test_multiple_validations():
    """Test multiple validations to check consistency"""

    print("\n" + "=" * 80)
    print("TEST 3: Multiple Validations (Performance Consistency)")
    print("=" * 80)

    times = []
    iterations = 5

    for i in range(iterations):
        start = time.time()
        result = v31_validator({
            "scanner_code": REAL_V31_SCANNER,
            "strict_mode": False,
            "return_fixes": False
        })
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"  Iteration {i+1}: {elapsed:.3f}s")

    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    print(f"\n📊 Statistics:")
    print(f"  Average: {avg_time:.3f}s")
    print(f"  Min: {min_time:.3f}s")
    print(f"  Max: {max_time:.3f}s")
    print(f"  Range: {max_time - min_time:.3f}s")

    return avg_time


def test_non_compliant_scanner():
    """Test validator with non-compliant code (worst case)"""

    print("\n" + "=" * 80)
    print("TEST 4: v31_validator with NON-COMPLIANT Code (Worst Case)")
    print("=" * 80)

    # Create non-compliant scanner
    non_compliant = """
def getSymbols():
    return symbols

def process(df):
    return df[df['close'] > df['open']]

def combine(signals):
    return signals
"""

    start = time.time()
    result = v31_validator({
        "scanner_code": non_compliant,
        "return_fixes": True
    })
    elapsed = time.time() - start

    print(f"\n⏱️  Execution Time: {elapsed:.3f} seconds")
    print(f"✅ Status: {result.status}")
    print(f"📊 Compliance Score: {result.result['compliance_score']}")
    print(f"📋 Total Violations: {result.result['total_violations']}")

    return elapsed


def main():
    """Run all realistic performance tests"""

    print("\n" + "🚀 " * 40)
    print("REALISTIC PERFORMANCE TESTS FOR CORE SCANNER TOOLS")
    print("🚀 " * 40)

    # Test 1: Validate real V31 scanner
    time1 = test_v31_validator_realistic()

    # Test 2: Generate scanner with validation
    time2 = test_v31_generator_with_validation()

    # Test 3: Multiple validations
    time3 = test_multiple_validations()

    # Test 4: Non-compliant scanner
    time4 = test_non_compliant_scanner()

    # Summary
    print("\n" + "=" * 80)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 80)
    print(f"\nTest 1 - Validate 300+ line V31 scanner: {time1:.3f}s")
    print(f"Test 2 - Generate + Validate scanner: {time2:.3f}s")
    print(f"Test 3 - Average validation time: {time3:.3f}s")
    print(f"Test 4 - Validate non-compliant code: {time4:.3f}s")

    print("\n🎯 REALISTIC BENCHMARKS:")
    print(f"  v31_validator (300+ lines): {time1:.3f}s")
    print(f"  v31_scanner_generator + validation: {time2:.3f}s")
    print(f"  Average validation: {time3:.3f}s")

    print("\n✅ All tests completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
