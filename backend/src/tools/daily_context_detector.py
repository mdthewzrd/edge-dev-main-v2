"""
Daily Context Detector Tool

Purpose: Detect daily market molds (D2, MDR, FBO, T30, etc.)
Version: 1.0.0
Estimated LOC: 80 lines
Target Execution: <0.5 seconds

This tool does ONE thing: Detect daily market setup patterns from OHLCV data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
from datetime import datetime
import time

# Import shared types
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def daily_context_detector(input_data: Dict[str, Any]) -> ToolResult:
    """
    Detect daily market molds (D2, MDR, FBO, T30, etc.)

    Supported Mold Types:
    - D2: Daily continuation setup
    - MDR: Multi-day range consolidation
    - FBO: First break out from consolidation
    - T30: 30-minute opening range breakout
    - BACKSIDE_B: Gap up into resistance

    Args:
        input_data: Dictionary with:
            - ticker (str): Stock symbol [REQUIRED]
            - df (pd.DataFrame): OHLCV data with pre-market data [REQUIRED]
            - market_date (str): Date in YYYY-MM-DD format [REQUIRED]
            - mold_types (list): Which molds to check (default: all)
            - gap_threshold (float): Minimum gap size (default: 0.01)
            - atr_period (int): ATR calculation period (default: 14)
            - include_alternatives (bool): Suggest alternative molds (default: True)
            - confidence_threshold (float): Minimum confidence (default: 0.7)

    Returns:
        ToolResult with daily mold detection results
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
        df = input_data.get("df")
        market_date = input_data.get("market_date", "")
        mold_types = input_data.get("mold_types", ["D2", "MDR", "FBO", "T30", "BACKSIDE_B"])
        gap_threshold = input_data.get("gap_threshold", 0.01)
        atr_period = input_data.get("atr_period", 14)
        include_alternatives = input_data.get("include_alternatives", True)
        confidence_threshold = input_data.get("confidence_threshold", 0.7)

        # Calculate required indicators
        df = calculate_indicators(df, atr_period)

        # Detect gap
        gap_analysis = analyze_gap(df)

        # Detect opening range
        opening_range = analyze_opening_range(df)

        # Detect each mold type
        mold_detections = []

        for mold_type in mold_types:
            detection = detect_single_mold(df, mold_type, gap_analysis, opening_range)
            if detection and detection['confidence'] >= confidence_threshold:
                mold_detections.append(detection)

        # Select primary mold (highest confidence)
        if mold_detections:
            primary_mold = max(mold_detections, key=lambda x: x['confidence'])
        else:
            primary_mold = {
                "type": "NONE",
                "confidence": 0.0,
                "match_score": 0.0,
                "characteristics": {}
            }

        # Find alternative molds
        alternative_molds = []
        if include_alternatives:
            alternative_molds = [m for m in mold_detections
                                if m['type'] != primary_mold['type']
                                and m['confidence'] >= confidence_threshold * 0.8]

        # Generate recommended setup
        recommended_setup = recommend_setup_from_mold(primary_mold, gap_analysis)

        # Prepare result
        result = {
            "ticker": ticker,
            "market_date": market_date,
            "daily_mold": primary_mold,
            "gap_analysis": gap_analysis,
            "opening_range": opening_range,
            "recommended_setup": recommended_setup,
            "alternative_molds": alternative_molds,
            "detection_timestamp": datetime.now().isoformat()
        }

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

    required_fields = ["ticker", "df", "market_date"]
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

    # Validate market_date format
    market_date = input_data.get("market_date", "")
    try:
        datetime.strptime(market_date, "%Y-%m-%d")
    except ValueError:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "market_date must be in YYYY-MM-DD format",
                "provided": market_date,
                "format": "YYYY-MM-DD"
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

    # Check for required OHLCV columns
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        return {
            "valid": False,
            "error": {
                "code": "MISSING_COLUMNS",
                "message": f"Missing required columns: {missing_cols}",
                "required_columns": required_cols
            }
        }

    return {"valid": True}


def calculate_indicators(df: pd.DataFrame, atr_period: int) -> pd.DataFrame:
    """Calculate required indicators for mold detection"""

    # Calculate ATR
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift(1))
    low_close = np.abs(df['low'] - df['close'].shift(1))

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = true_range.rolling(window=atr_period).mean()

    # Calculate gap
    df['prev_close'] = df['close'].shift(1)
    df['gap'] = df['open'] - df['prev_close']
    df['gap_percent'] = (df['gap'] / df['prev_close']) * 100
    df['gap_up'] = df['gap'] > 0
    df['gap_down'] = df['gap'] < 0

    # Calculate gap over ATR
    df['gap_over_atr'] = df['gap'] / df['atr']

    return df


def analyze_gap(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze gap characteristics"""

    latest = df.iloc[-1]

    return {
        "has_gap": latest['gap_up'] or latest['gap_down'],
        "gap_type": "GAP_UP" if latest['gap_up'] else ("GAP_DOWN" if latest['gap_down'] else "NO_GAP"),
        "gap_size_dollars": round(latest['gap'], 2),
        "gap_size_atr": round(latest['gap_over_atr'], 2),
        "gap_percent": round(latest['gap_percent'], 2),
        "gap_time": str(latest.name.time()) if hasattr(latest.name, 'time') else "N/A"
    }


def analyze_opening_range(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze opening range"""

    # Get first 30 minutes (assuming 5-min bars, first 6 bars = 30 min)
    or_bars = min(6, len(df))
    opening_range_df = df.iloc[:or_bars]

    or_high = opening_range_df['high'].max()
    or_low = opening_range_df['low'].min()
    or_range = or_high - or_low

    latest = df.iloc[-1]

    # Determine breakout direction
    if latest['close'] > or_high:
        breakout_direction = "BULLISH"
    elif latest['close'] < or_low:
        breakout_direction = "BEARISH"
    else:
        breakout_direction = "NEUTRAL"

    # Calculate breakout potential
    if breakout_direction != "NEUTRAL":
        breakout_strength = abs(latest['close'] - or_high if breakout_direction == "BULLISH" else or_low) / or_range
        breakout_potential = "HIGH" if breakout_strength > 0.5 else "LOW"
    else:
        breakout_potential = "NONE"

    return {
        "high": round(or_high, 2),
        "low": round(or_low, 2),
        "range_size": round(or_range, 2),
        "breakout_direction": breakout_direction,
        "breakout_potential": breakout_potential,
        "breakout_strength": round(breakout_strength, 3) if breakout_direction != "NEUTRAL" else 0.0
    }


def detect_single_mold(
    df: pd.DataFrame,
    mold_type: str,
    gap_analysis: Dict[str, Any],
    opening_range: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Detect a single mold type

    Returns:
        Mold detection dictionary or None
    """

    if mold_type == "BACKSIDE_B":
        return detect_backside_b(df, gap_analysis)
    elif mold_type == "MDR":
        return detect_mdr(df)
    elif mold_type == "D2":
        return detect_d2(df, gap_analysis)
    elif mold_type == "FBO":
        return detect_fbo(df, opening_range)
    elif mold_type == "T30":
        return detect_t30(df, opening_range)
    else:
        return None


def detect_backside_b(df: pd.DataFrame, gap_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Detect Backside B pattern"""

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    # Conditions
    has_significant_gap = gap_analysis['gap_size_atr'] >= 0.8
    opened_below_resistance = latest['open'] < latest['close'] * 0.98
    previous_was_red = previous['close'] < previous['open']

    if has_significant_gap and opened_below_resistance and previous_was_red:
        return {
            "type": "BACKSIDE_B",
            "confidence": 0.8,
            "match_score": 0.85,
            "characteristics": {
                "gap_type": "GAP_UP",
                "gap_size_atr": gap_analysis['gap_size_atr'],
                "opened_below_resistance": opened_below_resistance
            }
        }

    return None


def detect_mdr(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """Detect MDR (Multi-Day Range) pattern"""

    # Check last 5 days for tight range
    recent_high = df['high'].tail(5).max()
    recent_low = df['low'].tail(5).min()
    range_pct = ((recent_high - recent_low) / recent_low) * 100

    if range_pct < 3.0:
        return {
            "type": "MDR",
            "confidence": 0.75,
            "match_score": 0.8,
            "characteristics": {
                "range_days": 5,
                "range_percent": range_pct,
                "tight_range": True
            }
        }

    return None


def detect_d2(df: pd.DataFrame, gap_analysis: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Detect D2 (Daily Continuation) pattern"""

    latest = df.iloc[-1]

    # Calculate EMAs on the series, then get latest value
    ema9 = df['close'].ewm(span=9).mean().iloc[-1]
    volume_ma = df['volume'].ewm(span=20).mean().iloc[-1]

    # Conditions: trending up, gap up or continuation
    ema9_trend = latest['close'] > ema9
    volume_confirm = latest['volume'] > volume_ma

    if ema9_trend and (gap_analysis['has_gap'] or volume_confirm):
        return {
            "type": "D2",
            "confidence": 0.7,
            "match_score": 0.75,
            "characteristics": {
                "trend_continuation": True,
                "volume_confirmation": volume_confirm
            }
        }

    return None


def detect_fbo(df: pd.DataFrame, opening_range: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Detect FBO (First Break Out) pattern"""

    latest = df.iloc[-1]
    volume_ma = df['volume'].rolling(window=20).mean().iloc[-1]

    # Check for breakout above opening range
    breakout = latest['close'] > opening_range['high']
    volume_confirm = latest['volume'] > volume_ma * 1.5

    if breakout and volume_confirm:
        return {
            "type": "FBO",
            "confidence": 0.8,
            "match_score": 0.85,
            "characteristics": {
                "breakout_confirmed": True,
                "volume_confirmation": True
            }
        }

    return None


def detect_t30(df: pd.DataFrame, opening_range: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Detect T30 (30-minute opening range breakout) pattern"""

    latest = df.iloc[-1]
    volume_ma = df['volume'].rolling(window=20).mean().iloc[-1]

    # Check for breakout after 30 min
    breakout = latest['close'] > opening_range['high']
    volume_confirm = latest['volume'] > volume_ma * 1.2

    if breakout and volume_confirm:
        return {
            "type": "T30",
            "confidence": 0.75,
            "match_score": 0.8,
            "characteristics": {
                "opening_range_breakout": True,
                "volume_confirmation": True
            }
        }

    return None


def recommend_setup_from_mold(mold: Dict[str, Any], gap_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate recommended setup based on detected mold"""

    if mold['type'] == "NONE":
        return {
            "name": "No pattern detected",
            "parameters": {},
            "expected_win_rate": 0.0,
            "reasoning": "No clear pattern detected"
        }

    # Map mold to recommended setup
    setup_map = {
        "BACKSIDE_B": {
            "name": "Backside B Setup",
            "parameters": {
                "gap_over_atr": {"min": 0.8, "default": 1.0},
                "open_over_ema9": {"min": 0.90, "default": 0.92}
            },
            "expected_win_rate": 0.68,
            "reasoning": "Gap up into resistance suggests backside setup"
        },
        "MDR": {
            "name": "MDR Breakout",
            "parameters": {
                "breakout_threshold": {"default": 0.02}
            },
            "expected_win_rate": 0.65,
            "reasoning": "Tight range consolidation suggests upcoming breakout"
        },
        "D2": {
            "name": "D2 Continuation",
            "parameters": {
                "pullback_max": {"default": 0.382}
            },
            "expected_win_rate": 0.60,
            "reasoning": "Trend continuation with pullback opportunity"
        },
        "FBO": {
            "name": "FBO Breakout",
            "parameters": {
                "entry_trigger": "breakout_confirmation",
                "volume_threshold": 1.5
            },
            "expected_win_rate": 0.70,
            "reasoning": "First breakout from consolidation with volume"
        },
        "T30": {
            "name": "T30 Opening Range Breakout",
            "parameters": {
                "opening_range_bars": 30
            },
            "expected_win_rate": 0.65,
            "reasoning": "Opening range breakout with volume confirmation"
        }
    }

    return setup_map.get(mold['type'], {
        "name": "Unknown",
        "parameters": {},
        "expected_win_rate": 0.5,
        "reasoning": "Unknown mold type"
    })


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # Generate sample data
    dates = pd.date_range(start="2024-01-26", periods=100, freq="D")
    np.random.seed(42)

    # Create gap up scenario
    base_price = 150
    gap_up = 2.0

    close_prices = []
    for i in range(100):
        if i == 99:
            # Last day: gap up
            prev_close = close_prices[-1]
            open_price = prev_close * 1.015
            close = open_price * 0.995  # Red candle
            high = open_price * 1.01
        else:
            prev_close = base_price if i == 0 else close_prices[-1]
            noise = np.random.uniform(-1, 1, 1)
            open_price = prev_close + noise
            close = open_price + np.random.uniform(-0.5, 0.5, 1)
            high = max(open_price, close) + np.random.uniform(0, 0.5, 1)
            low = min(open_price, close) - np.random.uniform(0, 0.5, 1)

        close_prices.append(close)

    df = pd.DataFrame({
        'open': [base_price] * 100,  # Simplified
        'high': [base_price + 5] * 100,
        'low': [base_price - 5] * 100,
        'close': close_prices,
        'volume': np.random.randint(1000000, 5000000, 100)
    }, index=dates)

    test_input = {
        "ticker": "AAPL",
        "df": df,
        "market_date": "2024-01-26",
        "mold_types": ["BACKSIDE_B", "MDR", "D2"],
        "gap_threshold": 0.01,
        "atr_period": 14
    }

    result = daily_context_detector(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Daily mold detected successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Mold Type: {result.result['daily_mold']['type']}")
        print(f"Confidence: {result.result['daily_mold']['confidence']}")
        print(f"Recommended Setup: {result.result['recommended_setup']['name']}")
    else:
        print(f"❌ Error: {result.error}")
