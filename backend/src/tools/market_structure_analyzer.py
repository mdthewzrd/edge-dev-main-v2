"""
Market Structure Analyzer Tool

Purpose: Detect pivots, trends, support/resistance levels
Version: 1.0.0
Estimated LOC: 120 lines
Target Execution: <1 second

This tool does ONE thing: Analyze market structure from OHLCV data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
import time

# Import shared types
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def market_structure_analyzer(input_data: Dict[str, Any]) -> ToolResult:
    """
    Analyze market structure: pivots, trends, support/resistance levels

    Args:
        input_data: Dictionary with:
            - ticker (str): Stock symbol [REQUIRED]
            - df (pd.DataFrame): OHLCV data [REQUIRED]
            - lookback_period (int): Bars for pivot detection (default: 50)
            - pivot_method (str): 'standard', 'fibonacci', 'woodie' (default: 'standard')
            - trend_method (str): 'hh_hl', 'ma_trend' (default: 'hh_hl')
            - support_levels (int): Number of support levels (default: 3)
            - resistance_levels (int): Number of resistance levels (default: 3)
            - min_swing_strength (float): Minimum swing % (default: 0.02)
            - return_chart_data (bool): Include chart data (default: False)

    Returns:
        ToolResult with market structure analysis
    """

    start_time = time.time()
    tool_version = "1.0.0"

    try:
        # Validate input
        validation_result = validate_input(input_data)
        if not validation_result["valid"]:
            return ToolResult(
                status=ToolStatus.ERROR,
                result=None,
                error=validation_result["error"],
                warnings=None,
                execution_time=time.time() - start_time,
                tool_version=tool_version
            )

        # Extract inputs
        ticker = input_data.get("ticker", "")
        df = input_data.get("df").copy()  # Work on a copy
        lookback_period = input_data.get("lookback_period", 50)
        pivot_method = input_data.get("pivot_method", "standard")
        trend_method = input_data.get("trend_method", "hh_hl")
        support_levels = input_data.get("support_levels", 3)
        resistance_levels = input_data.get("resistance_levels", 3)
        min_swing_strength = input_data.get("min_swing_strength", 0.02)
        return_chart_data = input_data.get("return_chart_data", False)

        # Ensure DataFrame has DatetimeIndex if 'date' column exists
        if 'date' in df.columns and not isinstance(df.index, pd.DatetimeIndex):
            df['date'] = pd.to_datetime(df['date'])
            df = df.set_index('date')
        elif not isinstance(df.index, pd.DatetimeIndex):
            # If no date column, create DatetimeIndex from data
            df.index = pd.date_range(start='2024-01-01', periods=len(df), freq='D')

        # Analyze trend
        trend_analysis = analyze_trend(df, trend_method, lookback_period)

        # Detect pivot points
        pivot_highs, pivot_lows = detect_pivots(df, lookback_period, min_swing_strength)

        # Calculate support and resistance levels
        support_levels_list = calculate_support_levels(df, support_levels)
        resistance_levels_list = calculate_resistance_levels(df, resistance_levels)

        # Determine current position
        current_position = determine_current_position(df, trend_analysis, support_levels_list, resistance_levels_list)

        # Prepare result
        result = {
            "ticker": ticker,
            "analysis_period": {
                "start_date": str(df.index[0].date()),
                "end_date": str(df.index[-1].date()),
                "bars_analyzed": len(df)
            },
            "trend": trend_analysis,
            "pivot_highs": pivot_highs,
            "pivot_lows": pivot_lows,
            "support_levels": support_levels_list,
            "resistance_levels": resistance_levels_list,
            "current_position": current_position
        }

        # Add chart data if requested
        if return_chart_data:
            result["chart_data"] = prepare_chart_data(df)

        return ToolResult(
            status=ToolStatus.SUCCESS,
            result=result,
            error=None,
            warnings=[],
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )

    except Exception as e:
        import traceback
        return ToolResult(
            status=ToolStatus.ERROR,
            result=None,
            error={
                "code": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc()
            },
            warnings=None,
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )


def validate_input(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate input parameters"""

    required_fields = ["ticker", "df"]
    for field in required_fields:
        if field not in input_data:
            return {
                "valid": False,
                "error": {
                    "code": "MISSING_PARAMETER",
                    "message": f"Required parameter '{field}' is missing",
                    "parameter": field
                }
            }

    # Validate DataFrame
    df = input_data.get("df")
    if df is None or not isinstance(df, pd.DataFrame):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "df must be a pandas DataFrame",
                "parameter": "df"
            }
        }

    # Check for OHLC columns
    required_cols = ['open', 'high', 'low', 'close']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return {
            "valid": False,
            "error": {
                "code": "MISSING_COLUMNS",
                "message": f"Missing required columns: {missing_cols}",
                "required_columns": required_cols,
                "missing_columns": missing_cols
            }
        }

    # Check for sufficient data
    if len(df) < 20:
        return {
            "valid": False,
            "error": {
                "code": "INSUFFICIENT_DATA",
                "message": f"Insufficient data: need at least 20 bars, got {len(df)}",
                "minimum_required": 20
            }
        }

    return {"valid": True}


def analyze_trend(df: pd.DataFrame, method: str, lookback_period: int) -> Dict[str, Any]:
    """
    Analyze trend direction and strength

    Returns:
        Dictionary with trend analysis data
    """

    if method == "hh_hl":
        return analyze_trend_hh_hl(df, lookback_period)
    elif method == "ma_trend":
        return analyze_trend_ma(df, lookback_period)
    else:
        raise ValueError(f"Unknown trend method: {method}")


def analyze_trend_hh_hl(df: pd.DataFrame, lookback: int) -> Dict[str, Any]:
    """
    Analyze trend using Higher Highs, Higher Lows method
    """

    # Detect higher highs
    df['is_higher_high'] = df['high'].rolling(window=lookback, center=False).max() == df['high']
    df['is_higher_low'] = df['low'].rolling(window=lookback, center=False).min() == df['low']

    # Count patterns
    higher_highs_count = df['is_higher_high'].rolling(window=5).sum().iloc[-1]
    higher_lows_count = df['is_higher_low'].rolling(window=5).sum().iloc[-1]

    # Determine trend direction
    recent_highs = df['is_higher_high'].tail(lookback).sum()
    recent_lows = df['is_higher_low'].tail(lookback).sum()

    if recent_highs > recent_lows:
        direction = "BULLISH"
        strength = recent_highs / lookback
    elif recent_lows > recent_highs:
        direction = "BEARISH"
        strength = recent_lows / lookback
    else:
        direction = "SIDEWAYS"
        strength = 0.5

    # Find trend start (most recent direction change)
    trend_changes = identify_trend_changes(df, lookback)
    trend_start = trend_changes[-1] if trend_changes else str(df.index[0].date())

    return {
        "direction": direction,
        "strength": round(strength, 2),
        "duration": int(recent_highs + recent_lows),  # Bars in current trend
        "higher_highs": int(higher_highs_count),
        "higher_lows": int(higher_lows_count),
        "trend_start": trend_start,
        "trend_quality": "STRONG" if strength > 0.6 else "WEAK"
    }


def analyze_trend_ma(df: pd.DataFrame, lookback: int) -> Dict[str, Any]:
    """
    Analyze trend using Moving Average method
    """

    # Calculate moving averages
    df['ma_fast'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ma_slow'] = df['close'].ewm(span=21, adjust=False).mean()

    # Determine trend based on MA alignment
    df['ma_bullish'] = df['ma_fast'] > df['ma_slow']
    df['ma_bearish'] = df['ma_fast'] < df['ma_slow']

    # Count bullish vs bearish bars
    recent_bullish = df['ma_bullish'].tail(lookback).sum()
    recent_bearish = df['ma_bearish'].tail(lookback).sum()

    if recent_bullish > recent_bearish:
        direction = "BULLISH"
        strength = recent_bullish / lookback
    elif recent_bearish > recent_bullish:
        direction = "BEARISH"
        strength = recent_bearish / lookback
    else:
        direction = "SIDEWAYS"
        strength = 0.5

    return {
        "direction": direction,
        "strength": round(strength, 2),
        "duration": int(recent_bullish + recent_bearish),
        "trend_quality": "STRONG" if strength > 0.6 else "WEAK"
    }


def detect_pivots(df: pd.DataFrame, lookback: int, min_strength: float) -> tuple:
    """
    Detect pivot highs and lows

    Returns:
        Tuple of (pivot_highs_list, pivot_lows_list)
    """

    pivot_highs = []
    pivot_lows = []

    # Detect pivot highs
    for i in range(lookback, len(df) - lookback):
        window_before = df['high'].iloc[i-lookback:i+lookback]
        window_after = df['high'].iloc[i-lookback:i+lookback+1]

        if (df['high'].iloc[i] == window_before.max() and
            df['high'].iloc[i] > window_after.max()):

            # Calculate strength
            low_in_window = window_before.min()
            strength = (df['high'].iloc[i] - low_in_window) / df['high'].iloc[i]

            if strength >= min_strength:
                pivot_type = "major" if strength > 0.05 else "minor"
                pivot_highs.append({
                    "date": str(df.index[i].date()),
                    "price": float(df['high'].iloc[i]),
                    "strength": round(strength, 3),
                    "type": pivot_type
                })

    # Detect pivot lows
    for i in range(lookback, len(df) - lookback):
        window_before = df['low'].iloc[i-lookback:i+lookback]
        window_after = df['low'].iloc[i-lookback:i+lookback+1]

        if (df['low'].iloc[i] == window_before.min() and
            df['low'].iloc[i] < window_after.min()):

            # Calculate strength
            high_in_window = window_before.max()
            strength = (high_in_window - df['low'].iloc[i]) / df['low'].iloc[i]

            if strength >= min_strength:
                pivot_type = "major" if strength > 0.05 else "minor"
                pivot_lows.append({
                    "date": str(df.index[i].date()),
                    "price": float(df['low'].iloc[i]),
                    "strength": round(strength, 3),
                    "type": pivot_type
                })

    # Sort by date
    pivot_highs = sorted(pivot_highs, key=lambda x: x['date'])
    pivot_lows = sorted(pivot_lows, key=lambda x: x['date'])

    return pivot_highs, pivot_lows


def calculate_support_levels(df: pd.DataFrame, num_levels: int) -> List[Dict[str, Any]]:
    """
    Calculate support levels from pivot lows

    Returns:
        List of support level dictionaries
    """

    pivot_lows = []

    # Detect pivot lows
    for i in range(10, len(df) - 10):
        window_before = df['low'].iloc[i-5:i+6]
        window_after = df['low'].iloc[i-5:i+6]

        if (df['low'].iloc[i] == window_before.min() and
            df['low'].iloc[i] <= window_after.min()):

            pivot_lows.append({
                "price": float(df['low'].iloc[i]),
                "date": str(df.index[i].date()),
                "strength": 0.0  # Will calculate
            })

    # Sort by price (ascending), then recency
    pivot_lows.sort(key=lambda x: x['price'])

    # Calculate strength for each pivot (number of tests)
    for pivot in pivot_lows:
        tests = sum(1 for i in range(len(df))
                     if abs(df['low'].iloc[i] - pivot['price']) < pivot['price'] * 0.01)

        pivot['strength'] = round(tests / len(df) * 100, 1)
        pivot['tests'] = tests

    # Filter by tests (must be tested at least twice)
    tested_pivots = [p for p in pivot_lows if p['tests'] >= 2]

    # Get top N strongest support levels
    support_levels = sorted(tested_pivots, key=lambda x: x['strength'], reverse=True)[:num_levels]

    # Format output
    result = []
    for i, level in enumerate(support_levels):
        result.append({
            "level": i + 1,
            "price": round(level['price'], 2),
            "strength": round(level['strength'], 2),
            "tests": level['tests'],
            "last_test_date": level['date']
        })

    return result


def calculate_resistance_levels(df: pd.DataFrame, num_levels: int) -> List[Dict[str, Any]]:
    """
    Calculate resistance levels from pivot highs

    Returns:
        List of resistance level dictionaries
    """

    pivot_highs = []

    # Detect pivot highs
    for i in range(10, len(df) - 10):
        window_before = df['high'].iloc[i-5:i+6]
        window_after = df['high'].iloc[i-5:i+6]

        if (df['high'].iloc[i] == window_before.max() and
            df['high'].iloc[i] >= window_after.max()):

            pivot_highs.append({
                "price": float(df['high'].iloc[i]),
                "date": str(df.index[i].date()),
                "strength": 0.0
            })

    # Sort by price (descending), then recency
    pivot_highs.sort(key=lambda x: x['price'], reverse=True)

    # Calculate strength
    for pivot in pivot_highs:
        tests = sum(1 for i in range(len(df))
                     if abs(df['high'].iloc[i] - pivot['price']) < pivot['price'] * 0.01)

        pivot['strength'] = round(tests / len(df) * 100, 1)
        pivot['tests'] = tests

    # Filter and get top N
    tested_pivots = [p for p in pivot_highs if p['tests'] >= 2]
    resistance_levels = sorted(tested_pivots, key=lambda x: x['strength'], reverse=True)[:num_levels]

    # Format output
    result = []
    for i, level in enumerate(resistance_levels):
        result.append({
            "level": i + 1,
            "price": round(level['price'], 2),
            "strength": round(level['strength'], 2),
            "tests": level['tests'],
            "last_test_date": level['date']
        })

    return result


def determine_current_position(
    df: pd.DataFrame,
    trend_analysis: Dict[str, Any],
    support_levels: List[Dict[str, Any]],
    resistance_levels: List[Dict[str, Any]]
) -> Dict[str, Any]:

    latest = df.iloc[-1]

    # Distance to nearest support
    if support_levels:
        nearest_support = support_levels[0]
        dist_to_support = round((latest['close'] - nearest_support['price']) / latest['close'] * 100, 2)
    else:
        dist_to_support = round(latest['low'] / latest['close'] * 100, 2)

    # Distance to nearest resistance
    if resistance_levels:
        nearest_resistance = resistance_levels[0]
        dist_to_resistance = round((nearest_resistance['price'] - latest['close']) / latest['close'] * 100, 2)
    else:
        dist_to_resistance = round(latest['high'] / latest['close'] * 100, 2)

    # Determine position relative to levels
    if dist_to_resistance < 0.5:
        near_level = "RESISTANCE"
        near_level_price = nearest_resistance['price']
    elif dist_to_support < 0.5:
        near_level = "SUPPORT"
        near_level_price = nearest_support['price']
    else:
        near_level = "MIDDLE"
        near_level_price = latest['close']

    return {
        "relative_to_trend": f"In {trend_analysis['direction'].lower()} trend",
        "near_level": near_level,
        "near_level_price": round(near_level_price, 2),
        "distance_to_support_pct": dist_to_support,
        "distance_to_resistance_pct": dist_to_resistance
    }


def identify_trend_changes(df: pd.DataFrame, lookback: int) -> List[str]:
    """
    Identify when trend direction changed
    """

    # Simple approach: count consecutive HH/HL vs LL/LH
    trend_changes = []

    current_direction = None
    bars_in_direction = 0

    for i in range(lookback, len(df)):
        # Check for higher high and higher low
        if (df['high'].iloc[i] == df['high'].iloc[i-lookback:i].max() and
            df['low'].iloc[i] == df['low'].iloc[i-lookback:i].min()):

            new_direction = "UPTREND"

        # Check for lower high and lower low
        elif (df['high'].iloc[i] == df['high'].iloc[i-lookback:i].min() and
              df['low'].iloc[i] == df['low'].iloc[i-lookback:i].max()):

            new_direction = "DOWNTREND"

        else:
            new_direction = "SIDEWAYS"

        # Detect direction change
        if new_direction != current_direction:
            if current_direction is not None:
                trend_changes.append(str(df.index[i].date()))
            current_direction = new_direction
            bars_in_direction = 0
        else:
            bars_in_direction += 1

    return trend_changes


def prepare_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for charting"""

    return {
        "dates": df.index.tolist(),
        "high": df['high'].tolist(),
        "low": df['low'].tolist(),
               "close": df['close'].tolist(),
        "volume": df['volume'].tolist()
    }


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # Generate sample data with uptrend
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    np.random.seed(42)

    # Generate uptrend data
    close_prices = np.linspace(100, 150, 100)
    high_noise = np.random.uniform(0, 5, 100)
    low_noise = np.random.uniform(-5, 0, 100)

    df = pd.DataFrame({
        'open': close_prices + np.random.uniform(-2, 2, 100),
        'high': close_prices + high_noise,
        'low': close_prices + low_noise,
        'close': close_prices,
        'volume': np.random.randint(1000000, 5000000, 100)
    }, index=dates)

    test_input = {
        "ticker": "AAPL",
        "df": df,
        "lookback_period": 20,
        "support_levels": 3,
        "resistance_levels": 3,
        "min_swing_strength": 0.02
    }

    result = market_structure_analyzer(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Market structure analyzed successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Trend: {result.result['trend']['direction']}")
        print(f"Pivot Highs: {len(result.result['pivot_highs'])}")
        print(f"Pivot Lows: {len(result.result['pivot_lows'])}")
        print(f"Support Levels: {len(result.result['support_levels'])}")
        print(f"Resistance Levels: {len(result.result['resistance_levels'])}")
    else:
        print(f"❌ Error: {result.error}")
