"""
Indicator Calculator Tool

Purpose: Calculate user's proprietary indicators (RahulLines Cloud, Deviation Bands, etc.)
Version: 1.0.0
Estimated LOC: 100 lines
Target Execution: <0.5 seconds

This tool does ONE thing: Calculate proprietary technical indicators from OHLCV data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
import time

# Import shared types - handle both relative and absolute imports
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def indicator_calculator(input_data: Dict[str, Any]) -> ToolResult:
    """
    Calculate user's proprietary indicators from OHLCV data

    Supported Indicators:
    - 72_89_cloud: RahulLines 72/89 EMA cloud
    - 9_20_cloud: RahulLines 9/20 EMA cloud
    - deviation_bands: Standard deviation bands around mean

    Args:
        input_data: Dictionary with:
            - ticker (str): Stock symbol [REQUIRED]
            - df (pd.DataFrame): OHLCV data [REQUIRED]
            - indicators (list): List of indicators to calculate [REQUIRED]
            - lookback_period (int): Bars for calculation (default: 50)
            - return_type (str): 'dataframe', 'series', or 'dict' (default: 'dataframe')

    Returns:
        ToolResult with calculated indicators
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
        indicators = input_data.get("indicators", [])
        lookback_period = input_data.get("lookback_period", 50)
        return_type = input_data.get("return_type", "dataframe")

        # Calculate requested indicators
        calculated_indicators = {}

        for indicator in indicators:
            if indicator == "72_89_cloud":
                result = calculate_72_89_cloud(df, lookback_period)
                calculated_indicators["72_89_cloud"] = result

            elif indicator == "9_20_cloud":
                result = calculate_9_20_cloud(df, lookback_period)
                calculated_indicators["9_20_cloud"] = result

            elif indicator == "deviation_bands":
                result = calculate_deviation_bands(df, lookback_period)
                calculated_indicators["deviation_bands"] = result

            else:
                # Unknown indicator
                return ToolResult(
                    status=ToolStatus.ERROR,
                    result=None,
                    error={
                        "code": "INVALID_INDICATOR",
                        "message": f"Unknown indicator: {indicator}",
                        "supported_indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"]
                    },
                    warnings=None,
                    execution_time=time.time() - start_time,
                    tool_version=tool_version
                )

        # Format output based on return_type
        result = format_output(calculated_indicators, ticker, return_type)

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

    # Check required fields
    required_fields = ["ticker", "df", "indicators"]
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

    # Validate indicators
    indicators = input_data.get("indicators", [])
    if not indicators:
        return {
            "valid": False,
            "error": {
                "code": "MISSING_PARAMETER",
                "message": "No indicators specified",
                "parameter": "indicators",
                "supported_indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"]
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
                "parameter": "df",
                "expected_type": "pd.DataFrame"
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
                "required_columns": required_cols,
                "missing_columns": missing_cols
            }
        }

    # Check for sufficient data
    lookback_period = input_data.get("lookback_period", 50)
    if len(df) < lookback_period:
        return {
            "valid": False,
            "error": {
                "code": "INSUFFICIENT_DATA",
                "message": f"Insufficient data: need {lookback_period} bars, got {len(df)}",
                "required": lookback_period,
                "provided": len(df)
            }
        }

    return {"valid": True}


def calculate_72_89_cloud(df: pd.DataFrame, period: int = 50) -> Dict[str, Any]:
    """
    Calculate RahulLines 72/89 EMA Cloud

    Args:
        df: DataFrame with OHLCV data
        period: Lookback period for EMA calculation

    Returns:
        Dictionary with cloud data (upper, lower, current position)
    """

    # Calculate EMAs
    df['ema72'] = df['close'].ewm(span=72, adjust=False).mean()
    df['ema89'] = df['close'].ewm(span=89, adjust=False).mean()

    # Get latest values
    latest_upper = df['ema72'].iloc[-1]
    latest_lower = df['ema89'].iloc[-1]
    latest_close = df['close'].iloc[-1]

    # Determine current position
    if latest_close > latest_upper:
        position = "Above cloud"
    elif latest_close < latest_lower:
        position = "Below cloud"
    else:
        position = "Inside cloud"

    # Prepare cloud data for charting
    cloud_data = {
        "dates": df.index.tolist(),
        "upper_values": df['ema72'].tolist(),
        "lower_values": df['ema89'].tolist(),
    }

    return {
        "upper": df['ema72'],
        "lower": df['ema89'],
        "cloud_data": cloud_data,
        "current_position": position,
        "latest_upper": latest_upper,
        "latest_lower": latest_lower,
        "latest_close": latest_close
    }


def calculate_9_20_cloud(df: pd.DataFrame, period: int = 50) -> Dict[str, Any]:
    """
    Calculate RahulLines 9/20 EMA Cloud

    Args:
        df: DataFrame with OHLCV data
        period: Lookback period for EMA calculation

    Returns:
        Dictionary with cloud data
    """

    # Calculate EMAs
    df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema20'] = df['close'].ewm(span=20, adjust=False).mean()

    # Get latest values
    latest_upper = df['ema9'].iloc[-1]
    latest_lower = df['ema20'].iloc[-1]
    latest_close = df['close'].iloc[-1]

    # Determine current position
    if latest_close > latest_upper:
        position = "Above cloud"
    elif latest_close < latest_lower:
        position = "Below cloud"
    else:
        position = "Inside cloud"

    return {
        "upper": df['ema9'],
        "lower": df['ema20'],
        "cloud_data": {
            "dates": df.index.tolist(),
            "upper_values": df['ema9'].tolist(),
            "lower_values": df['ema20'].tolist()
        },
        "current_position": position,
        "latest_upper": latest_upper,
        "latest_lower": latest_lower
    }


def calculate_deviation_bands(df: pd.DataFrame, period: int = 20, num_stds: float = 2.0) -> Dict[str, Any]:
    """
    Calculate Standard Deviation Bands

    Args:
        df: DataFrame with OHLCV data
        period: Lookback period for mean/std calculation
        num_stds: Number of standard deviations for bands

    Returns:
        Dictionary with deviation bands (upper, lower, mean, std)
    """

    # Calculate mean and std deviation
    mean = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()

    # Calculate bands
    upper = mean + (std * num_stds)
    lower = mean - (std * num_stds)

    return {
        "upper": upper,
        "lower": lower,
        "mean": mean,
        "std": std,
        "width": upper - lower
    }


def format_output(indicators: Dict[str, Any], ticker: str, return_type: str) -> Dict[str, Any]:
    """Format output based on return_type preference"""

    if return_type == "dict":
        # Return simplified dict format
        result = {
            "ticker": ticker,
            "indicators": {}
        }

        for indicator_name, indicator_data in indicators.items():
            if "cloud_data" in indicator_data:
                # For clouds, return summary only
                result["indicators"][indicator_name] = {
                    "upper": indicator_data["latest_upper"],
                    "lower": indicator_data["latest_lower"],
                    "position": indicator_data["current_position"]
                }
            else:
                result["indicators"][indicator_name] = indicator_data

        return result

    elif return_type == "series":
        # Return pandas Series format
        result = {
            "ticker": ticker,
            "indicators": {}
        }

        for indicator_name, indicator_data in indicators.items():
            # Extract latest values
            if "upper" in indicator_data:
                result["indicators"][indicator_name] = {
                    "upper": indicator_data["upper"].iloc[-1],
                    "lower": indicator_data["lower"].iloc[-1]
                }

        return result

    else:  # dataframe (default)
        # Return full DataFrame format
        return {
            "ticker": ticker,
            "indicators": indicators,
            "calculation_time": time.time(),
            "data_points": len(indicators.get("72_89_cloud", {}).get("upper", [])),
        }


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    # Generate sample data
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    np.random.seed(42)

    df = pd.DataFrame({
        'open': np.random.uniform(140, 160, 100),
        'high': np.random.uniform(160, 180, 100),
        'low': np.random.uniform(120, 140, 100),
        'close': np.random.uniform(140, 160, 100),
        'volume': np.random.randint(1000000, 5000000, 100)
    }, index=dates)

    test_input = {
        "ticker": "AAPL",
        "df": df,
        "indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"],
        "lookback_period": 50
    }

    result = indicator_calculator(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Indicators calculated successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Ticker: {result.result['ticker']}")
        print(f"Calculated: {list(result.result['indicators'].keys())}")
    else:
        print(f"❌ Error: {result.error}")
