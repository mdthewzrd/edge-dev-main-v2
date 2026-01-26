# 🔧 Tool Interface Specifications
## Complete Implementation Guide for 13 Tools

**Date**: January 26, 2026
**Status**: ✅ TOOL INTERFACES COMPLETE
**Phase**: Task 1.3 - Tool Extraction & Testing (Week 1)
**Ready for**: Implementation (Task 2.1)

---

## 📋 TABLE OF CONTENTS

1. [Standard Tool Interface](#standard-tool-interface)
2. [Error Handling Standards](#error-handling-standards)
3. [Tool Specifications]((#tool-specifications)
   - Tool 1: v31_scanner_generator
   - Tool 2: v31_validator
   - Tool 3: scanner_executor
   - Tool 4: indicator_calculator
   - Tool 5: market_structure_analyzer
   - Tool 6: daily_context_detector
   - Tool 7: a_plus_analyzer
   - Tool 8: quick_backtester
   - Tool 9: knowledge_base_search
   - Tool 10: similar_strategy_finder
   - Tool 11: parameter_optimizer
   - Tool 12: position_risk_calculator
   - Tool 13: build_plan_generator
4. [Testing Framework](#testing-framework)
5. [Performance Benchmarks](#performance-benchmarks)

---

## 🎯 STANDARD TOOL INTERFACE

All 13 tools follow this standard interface:

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ToolStatus(Enum):
    """Standard tool execution status"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"  # Success but with warnings

@dataclass
class ToolResult:
    """Standard tool result structure"""
    status: ToolStatus
    result: Optional[Dict[str, Any]]
    error: Optional[Dict[str, str]]
    warnings: Optional[list]
    execution_time: float
    tool_version: str

def standard_tool_interface(
    tool_name: str,
    tool_version: str,
    input_data: Dict[str, Any],
    func: callable
) -> ToolResult:
    """
    Standard wrapper for all tool functions

    Args:
        tool_name: Name of the tool
        tool_version: Version string
        input_data: Validated input dictionary
        func: Core tool function to execute

    Returns:
        ToolResult with standardized structure
    """
    import time
    start_time = time.time()

    try:
        # Validate input
        validation_result = validate_input(tool_name, input_data)
        if not validation_result["valid"]:
            return ToolResult(
                status=ToolStatus.ERROR,
                result=None,
                error=validation_result["error"],
                warnings=None,
                execution_time=time.time() - start_time,
                tool_version=tool_version
            )

        # Execute tool function
        tool_result = func(input_data)

        return ToolResult(
            status=ToolStatus.SUCCESS,
            result=tool_result,
            error=None,
            warnings=tool_result.get("warnings", []),
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )

    except Exception as e:
        return ToolResult(
            status=ToolStatus.ERROR,
            result=None,
            error={
                "code": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc() if DEBUG else None
            },
            warnings=None,
            execution_time=time.time() - start_time,
            tool_version=tool_version
        )
```

---

## ⚠️ ERROR HANDLING STANDARDS

### Error Code System

```python
class ErrorCode(Enum):
    """Standard error codes for all tools"""
    # Input Errors (100-199)
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_PARAMETER = "MISSING_PARAMETER"
    INVALID_TYPE = "INVALID_TYPE"
    OUT_OF_RANGE = "OUT_OF_RANGE"

    # Data Errors (200-299)
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    DATA_FORMAT_ERROR = "DATA_FORMAT_ERROR"
    MISSING_COLUMNS = "MISSING_COLUMNS"

    # Execution Errors (300-399)
    EXECUTION_FAILED = "EXECUTION_FAILED"
    TIMEOUT = "TIMEOUT"
    OUT_OF_MEMORY = "OUT_OF_MEMORY"

    # External Service Errors (400-499)
    BACKEND_CONNECTION_FAILED = "BACKEND_CONNECTION_FAILED"
    ARCHON_CONNECTION_FAILED = "ARCHON_CONNECTION_FAILED"
    WEBSOCKET_ERROR = "WEBSOCKET_ERROR"

    # Validation Errors (500-599)
    VALIDATION_FAILED = "VALIDATION_FAILED"
    COMPLIANCE_ERROR = "COMPLIANCE_ERROR"
```

### Standard Error Response Format

```python
{
    "status": "error",
    "error": {
        "code": "MISSING_PARAMETER",
        "message": "Required parameter 'gap_over_atr' is missing",
        "parameter": "gap_over_atr",
        "expected_type": "float",
        "allowed_range": "0.5 to 2.0",
        "suggestion": "Provide gap_over_atr between 0.5 and 2.0 for optimal results"
    },
    "execution_time": 0.01,
    "tool_version": "1.0.0"
}
```

---

## 🔧 TOOL SPECIFICATIONS

---

### TOOL 1: `v31_scanner_generator`

**Version**: 1.0.0
**Purpose**: Generate V31-compliant scanner code from natural language or A+ examples
**Estimated LOC**: 150 lines

#### Input Specification

```python
{
    # Required
    "description": str,  # Natural language description

    # Optional
    "a_plus_example": {
        "image_url": str,  # Chart image URL (optional)
        "text_description": str,  # Text description instead of image
        "parameters": dict,  # Extracted parameters from A+ example
        "date": str  # ISO format YYYY-MM-DD
    },

    # Optional parameters
    "parameters": {
        "gap_over_atr": {
            "min": float,  # 0.8
            "max": float,  # 1.2
            "default": float  # 1.0
        },
        "open_over_ema9": {
            "min": float,
            "max": float,
            "default": float
        }
    },

    # Options
    "include_comments": True,  # Add explanatory comments
    "include_validation": True,  # Run v31_validator after generation
    "output_format": "python"  # python, json
}
```

#### Output Specification

```python
{
    "scanner_code": str,  # Complete V31 scanner code
    "code_structure": {
        "has_stage1": bool,
        "has_stage2": bool,
        "has_stage3": bool,
        "per_ticker_operations": bool,
        "smart_filters": bool
    },
    "v31_validated": bool,
    "validation_report": {
        "compliant": bool,
        "score": float,  # 0.0 to 1.0
        "violations": [],
        "warnings": []
    },
    "parameters_used": dict,
    "estimated_execution_time": str,  # "3 minutes for 5000 symbols"
    "estimated_signals": int,  # Expected signal count
    "warnings": []
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| MISSING_PARAMETER | `description` is empty | Description is required |
| INVALID_INPUT | `description` is too vague | Please provide more details about the scanner |
| DATA_FORMAT_ERROR | `a_plus_example` has invalid format | A+ example must have image or text |

#### Test Cases

```python
# Test 1: Basic scanner generation
input1 = {
    "description": "Backside scanner for gap ups with ATR filter"
}
# Expected: Valid V31 scanner code

# Test 2: With parameters
input2 = {
    "description": "Gap up scanner",
    "parameters": {
        "gap_over_atr": {"default": 0.8},
        "vol_mult": {"default": 1.2}
    }
}
# Expected: Scanner with those parameters

# Test 3: From A+ example
input3 = {
    "description": "Backside setup",
    "a_plus_example": {
        "text_description": "Gap up into resistance, red candle close",
        "parameters": {"gap_over_atr": 0.85}
    }
}
# Expected: Scanner matching A+ example

# Test 4: Invalid input (should fail)
input4 = {
    "description": ""
}
# Expected: MISSING_PARAMETER error
```

---

### TOOL 2: `v31_validator`

**Version**: 1.0.0
**Purpose**: Validate code against V31 Gold Standard
**Estimated LOC**: 80 lines

#### Input Specification

```python
{
    # Required
    "scanner_code": str,  # Python code to validate

    # Options
    "strict_mode": bool,  # Fail fast or warnings only
    "check_pillars": list,  # Which pillars to check [1, 2, 3, 4]
    "return_fixes": True  # Include fix suggestions
}
```

#### Output Specification

```python
{
    "is_v31_compliant": bool,
    "compliance_score": float,  # 0.0 to 1.0

    # Detailed results
    "pillar_results": {
        "pillar_0_market_scanning": {
            "compliant": bool,
            "score": float,
            "violations": [],
            "checks": {
                "full_market_coverage": bool,
                "grouped_endpoint_optimization": bool,
                "batch_processing": bool
            }
        },
        "pillar_1_3stage_architecture": {
            "compliant": bool,
            "score": float,
            "violations": [],
            "checks": {
                "has_stage1": bool,
                "has_stage2": bool,
                "has_stage3": bool
            }
        },
        "pillar_2_per_ticker_operations": {
            "compliant": bool,
            "score": float,
            "violations": [],
            "checks": {
                "independent_processing": bool,
                "smart_filters": bool,
                "no_lookahead_bias": bool
            }
        },
        "pillar_3_parallel_processing": {
            "compliant": bool,
            "score": float,
            "violations": [],
            "checks": {
                "parameter_system": bool,
                "code_structure": bool,
                "naming_conventions": bool
            }
        }
    },

    # Violations with fixes
    "violations": [
        {
            "pillar": "Pillar 1: 3-Stage Architecture",
            "severity": "CRITICAL",  # CRITICAL, MAJOR, MINOR
            "issue": "Missing stage2_process_symbols() function",
            "location": "Line 45",
            "fix_suggestion": "Add stage2 function that processes each ticker independently",
            "code_example": "def stage2_process_symbols(df): ..."
        }
    ],

    # Summary
    "total_violations": int,
    "critical_violations": int,
    "major_violations": int,
    "minor_violations": int,

    "warnings": []  # Non-blocking issues
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INVALID_INPUT | `scanner_code` is not valid Python | Code must be valid Python syntax |
| DATA_FORMAT_ERROR | `scanner_code` is not a string | Scanner code must be a string |
| MISSING_PARAMETER | `scanner_code` is empty | Scanner code is required |

#### Test Cases

```python
# Test 1: V31 compliant scanner
code1 = """
def get_stage1_symbols():
    return symbols

def stage2_process_symbols(df):
    return df[df['gap_over_atr'] > 0.8]

def aggregate_signals(signals):
    return signals
"""
# Expected: All pillars compliant

# Test 2: Missing stage2
code2 = """
def get_stage1_symbols():
    return symbols
"""
# Expected: CRITICAL violation - missing stage2

# Test 3: Invalid Python
code3 = "this is not valid python"
# Expected: INVALID_INPUT error

# Test 4: Non-compliant parameter names
code4 = """
def getStage1Symbols():  # wrong naming
    return symbols
"""
# Expected: MAJOR violation - naming convention
```

---

### TOOL 3: `scanner_executor`

**Version**: 1.0.0
**Purpose**: Execute scanner and collect results with progress tracking
**Estimated LOC**: 120 lines

#### Input Specification

```python
{
    # Required
    "scanner_code": str,
    "scan_date": str,  # ISO format YYYY-MM-DD

    # Required parameters
    "parameters": dict,

    # Backend connection
    "backend_url": str,  # http://localhost:8000
    "websocket_url": str,  # ws://localhost:8000/ws

    # Options
    "timeout": 300,  # seconds
    "poll_interval": 1,  # seconds (progress check frequency)
    "save_results": True,
    "output_format": "json"
}
```

#### Output Specification

```python
{
    "execution_id": str,  # UUID
    "status": str,  # QUEUED, RUNNING, COMPLETE, FAILED

    # Progress tracking
    "progress": {
        "stage": str,  # "Stage 1: Preliminary Fetch"
        "percent": int,  # 0-100
        "elapsed_seconds": float,
        "estimated_remaining": float,
        "current_symbol": str,  # "Processing AAPL..."
        "symbols_processed": int,
        "total_symbols": int
    },

    # Results (when complete)
    "results": {
        "scan_date": str,
        "total_signals": int,
        "signals": [
            {
                "ticker": "AAPL",
                "signal_time": "2024-01-26 09:45:00",
                "entry_price": 150.25,
                "parameters": {...},
                "confidence": 0.85
            }
        ],
        "metadata": {
            "symbols_scanned": 5000,
            "signals_found": 47,
            "execution_time": 180.5,
            "market_regime": "Bullish"
        }
    },

    # Error (if failed)
    "error": {
        "code": str,
        "message": str,
        "stage": str,  # Where it failed
        "partial_results": dict
    }
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| BACKEND_CONNECTION_FAILED | Cannot connect to backend | Backend is not responding |
| WEBSOCKET_ERROR | WebSocket connection lost | Lost connection to backend |
| TIMEOUT | Execution exceeded timeout limit | Scanner execution timed out |
| EXECUTION_FAILED | Scanner code has runtime error | Check scanner code for errors |

#### Test Cases

```python
# Test 1: Successful execution
input1 = {
    "scanner_code": scanner_code,
    "scan_date": "2024-01-26",
    "parameters": {"gap_over_atr": 0.8},
    "backend_url": "http://localhost:8000",
    "websocket_url": "ws://localhost:8000/ws"
}
# Expected: Complete with results

# Test 2: Backend not running (should fail gracefully)
input2 = {
    "scanner_code": scanner_code,
    "scan_date": "2024-01-26",
    "parameters": {"gap_over_atr": 0.8},
    "backend_url": "http://localhost:9999",  # wrong port
    "websocket_url": "ws://localhost:9999/ws"
}
# Expected: BACKEND_CONNECTION_FAILED error

# Test 3: Timeout
input3 = {
    "scanner_code": slow_scanner_code,
    "scan_date": "2024-01-26",
    "parameters": {"gap_over_atr": 0.8},
    "backend_url": "http://localhost:8000",
    "websocket_url": "ws://localhost:8000/ws",
    "timeout": 5  # 5 seconds
}
# Expected: TIMEOUT error
```

---

### TOOL 4: `indicator_calculator`

**Version**: 1.0.0
**Purpose**: Calculate user's proprietary indicators (RahulLines, Deviation Bands, etc.)
**Estimated LOC**: 100 lines

#### Input Specification

```python
{
    # Required
    "ticker": str,
    "df": pd.DataFrame,  # OHLCV data with columns: open, high, low, close, volume

    # Required columns
    "data": {
        "open": list,
        "high": list,
        "low": list,
        "close": list,
        "volume": list
    },  # Alternative: pass DataFrame directly

    # Required
    "indicators": list,  # ["72_89_cloud", "9_20_cloud", "deviation_bands"]

    # Options
    "lookback_period": 50,  # bars
    "return_type": "dataframe"  # dataframe, series, dict
}
```

#### Output Specification

```python
{
    "ticker": "AAPL",
    "indicators": {
        "72_89_cloud": {
            "upper": pd.Series,  # or list
            "lower": pd.Series,
            "cloud_data": {
                "dates": [],
                "upper_values": [],
                "lower_values": []
            },
            "current_position": "Inside cloud"
        },
        "9_20_cloud": {
            "upper": pd.Series,
            "lower": pd.Series
        },
        "deviation_bands": {
            "upper": pd.Series,
            "lower": pd.Series,
            "mean": pd.Series,
            "std": pd.Series
        }
    },
    "calculation_time": 0.05,  # seconds
    "data_points": 50,
    "warnings": []
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| MISSING_COLUMNS | OHLCV columns missing | Data must have open, high, low, close, volume |
| INSUFFICIENT_DATA | Less than lookback_period | Need at least 50 bars of data |
| INVALID_INDICATOR | Indicator name not recognized | Supported: 72_89_cloud, 9_20_cloud, deviation_bands |
| DATA_FORMAT_ERROR | Data cannot be converted to DataFrame | Invalid data format |

#### Test Cases

```python
# Test 1: Calculate 72/89 cloud
df = pd.DataFrame({
    'open': [150, 151, 152],
    'high': [152, 153, 154],
    'low': [149, 150, 151],
    'close': [151, 152, 153],
    'volume': [1000000, 1100000, 900000]
})

input1 = {
    "ticker": "AAPL",
    "df": df,
    "indicators": ["72_89_cloud"]
}
# Expected: Cloud data with upper/lower bands

# Test 2: Multiple indicators
input2 = {
    "ticker": "AAPL",
    "df": df,
    "indicators": ["72_89_cloud", "9_20_cloud", "deviation_bands"]
}
# Expected: All three indicators

# Test 3: Insufficient data
input3 = {
    "ticker": "AAPL",
    "df": df.head(10),  # Only 10 bars
    "indicators": ["72_89_cloud"]
}
# Expected: INSUFFICIENT_DATA error

# Test 4: Invalid indicator
input4 = {
    "ticker": "AAPL",
    "df": df,
    "indicators": ["invalid_indicator"]
}
# Expected: INVALID_INDICATOR error
```

---

### TOOL 5: `market_structure_analyzer`

**Version**: 1.0.0
**Purpose**: Detect pivots, trends, support/resistance levels
**Estimated LOC**: 120 lines

#### Input Specification

```python
{
    # Required
    "ticker": str,
    "df": pd.DataFrame,  # OHLCV data

    # Configuration
    "lookback_period": 50,  # bars for pivot detection
    "pivot_method": "standard",  # standard, fibonacci, woodie
    "trend_method": "higher_highs_higher_lows",  # hh_hl, ma_trend

    # Options
    "support_levels": 3,  # Number of support levels to find
    "resistance_levels": 3,
    "min_swing_strength": 0.02,  # Minimum swing % to be pivot
    "return_chart_data": False
}
```

#### Output Specification

```python
{
    "ticker": "AAPL",
    "analysis_period": {
        "start_date": "2024-01-01",
        "end_date": "2024-01-26",
        "bars_analyzed": 50
    },

    # Trend analysis
    "trend": {
        "direction": "BULLISH",  # BULLISH, BEARISH, SIDEWAYS
        "strength": 0.75,  # 0.0 to 1.0
        "duration": 18,  # bars in current trend
        "higher_highs": 5,
        "higher_lows": 4,
        "trend_start": "2024-01-15"
    },

    # Pivot points
    "pivot_highs": [
        {
            "date": "2024-01-10",
            "price": 158.50,
            "strength": 0.85,
            "type": "major"
        }
    ],
    "pivot_lows": [
        {
            "date": "2024-01-05",
            "price": 148.20,
            "strength": 0.78,
            "type": "minor"
        }
    ],

    # Support and resistance
    "support_levels": [
        {
            "level": 150.25,
            "strength": 0.82,
            "tests": 3,  # How many times tested
            "last_test": "2024-01-24"
        }
    ],
    "resistance_levels": [
        {
            "level": 158.20,
            "strength": 0.90,
            "tests": 2,
            "last_test": "2024-01-25"
        }
    ],

    # Current position
    "current_position": {
        "relative_to_trend": "In uptrend",
        "near_level": "RESISTANCE",
        "distance_to_support": 2.5,  # dollars
        "distance_to_resistance": 0.75
    },

    "warnings": ["Approaching resistance at 158.20"]
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INSUFFICIENT_DATA | Less than 20 bars | Need at least 20 bars for analysis |
| MISSING_COLUMNS | OHLC columns missing | Data must have open, high, low, close |
| SIDEWAYS_MARKET | No clear trend | Market is ranging, trend strength < 0.3 |

#### Test Cases

```python
# Test 1: Uptrend detection
df_uptrend = pd.DataFrame({
    'close': [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
})

input1 = {
    "ticker": "AAPL",
    "df": df_uptrend,
    "lookback_period": 10
}
# Expected: trend = BULLISH, strength > 0.7

# Test 2: Sideways market
df_sideways = pd.DataFrame({
    'close': [100, 101, 99, 100, 101, 100, 99, 100, 101, 100]
})

input2 = {
    "ticker": "AAPL",
    "df": df_sideways,
    "lookback_period": 10
}
# Expected: trend = SIDEWAYS, strength < 0.3

# Test 3: Insufficient data
input3 = {
    "ticker": "AAPL",
    "df": df.head(5),
    "lookback_period": 50
}
# Expected: INSUFFICIENT_DATA error
```

---

### TOOL 6: `daily_context_detector`

**Version**: 1.0.0
**Purpose**: Detect daily market molds (D2, MDR, FBO, T30, etc.)
**Estimated LOC**: 80 lines

#### Input Specification

```python
{
    # Required
    "ticker": str,
    "df": pd.DataFrame,  # OHLCV data with pre-market
    "market_date": str,  # YYYY-MM-DD

    # Configuration
    "mold_types": list,  # Which molds to check [D2, MDR, FBO, T30, etc.]
    "gap_threshold": 0.01,  # Minimum gap size (1% of price)
    "atr_period": 14,

    # Options
    "include_alternatives": True,  # Suggest alternative molds
    "confidence_threshold": 0.7
}
```

#### Output Specification

```python
{
    "ticker": "AAPL",
    "market_date": "2024-01-26",

    # Primary mold
    "daily_mold": {
        "type": "D2",
        "confidence": 0.85,
        "match_score": 0.82,
        "characteristics": {
            "gap_type": "GAP_UP",
            "gap_size": 1.5,  # ATR multiple
            "opening_range_broken": True
        }
    },

    # Gap analysis
    "gap_analysis": {
        "has_gap": True,
        "gap_type": "GAP_UP",
        "gap_size": 1.75,  # dollars
        "gap_size_atr": 1.5,
        "gap_percent": 1.17,
        "gap_time": "09:30:00"
    },

    # Opening range
    "opening_range": {
        "high": 152.50,
        "low": 150.20,
        "range_size": 2.30,
        "breakout_direction": "BULLISH",
        "breakout_potential": "HIGH"
    },

    # Recommended setup
    "recommended_setup": {
        "name": "Backside B",
        "parameters": {
            "gap_over_atr": 0.8,
            "open_over_ema9": 0.92
        },
        "expected_win_rate": 0.68,
        "reasoning": "Gap up into resistance suggests backside setup"
    },

    # Alternative molds
    "alternative_molds": [
        {
            "type": "MDR",
            "confidence": 0.62,
            "characteristics": "Multiple days range"
        }
    ],

    "warnings": []
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INSUFFICIENT_DATA | Missing pre-market data | Need pre-market data for mold detection |
| NO_CLEAR_MOLD | No mold matches criteria | Market conditions unclear |
| DATA_FORMAT_ERROR | Invalid DataFrame format | Data must have timestamp index |

#### Test Cases

```python
# Test 1: D2 mold (gap up)
df_d2 = pd.DataFrame({
    'gap': 2.0,
    'open': 152.0,  # Gapped up
    'prev_close': 150.0
})

input1 = {
    "ticker": "AAPL",
    "df": df_d2,
    "market_date": "2024-01-26",
    "mold_types": ["D2", "MDR", "FBO"]
}
# Expected: daily_mold = D2 with confidence > 0.7

# Test 2: No clear mold
input2 = {
    "ticker": "AAPL",
    "df": normal_day_df,  # No gap, normal range
    "market_date": "2024-01-26",
    "mold_types": ["D2", "MDR", "FBO"]
}
# Expected: NO_CLEAR_MOLD warning

# Test 3: Missing pre-market
input3 = {
    "ticker": "AAPL",
    "df": df_without_premarket,
    "market_date": "2024-01-26",
    "mold_types": ["D2"]
}
# Expected: INSUFFICIENT_DATA error
```

---

### TOOL 7: `a_plus_analyzer`

**Version**: 1.0.0
**Purpose**: Analyze A+ examples, extract parameters, validate against history
**Estimated LOC**: 100 lines

#### Input Specification

```python
{
    # Required
    "a_plus_example": {
        "image_url": str,  # OR use text_description
        "text_description": str,  # Alternative to image
        "chart_type": str,  # backside_euphoric_top, gap_continuation, etc.
        "date": str,  # YYYY-MM-DD
        "parameters": dict  # Pre-extracted (optional)
    },

    # Validation options
    "validate_historical": True,
    "historical_period_days": 30,  # Days to look back
    "min_occurrences": 5,  # Minimum similar patterns to find

    # Analysis options
    "extract_parameters": True,
    "suggest_optimization": True
}
```

#### Output Specification

```python
{
    "analysis": {
        "setup_detected": "Backside B Euphoric Top",
        "confidence": 0.88,

        # Parameters extracted
        "parameters_extracted": {
            "gap_over_atr": 0.8,
            "open_over_ema9": 0.92,
            "vol_mult": 1.2,
            "target_profit": 2.5,  # Risk multiple
            "stop_loss": 1.5  # Risk multiple
        },

        # Parameter ranges
        "parameter_ranges": {
            "gap_over_atr": {"min": 0.7, "max": 1.2, "optimal": 0.85},
            "open_over_ema9": {"min": 0.85, "max": 0.98, "optimal": 0.92}
        },

        # Chart features
        "features_identified": {
            "gap_up": True,
            "euphoric_top": True,
            "resistance_test": True,
            "volume_spike": True
        }
    },

    # Historical validation
    "historical_validation": {
        "similar_occurrences": 45,
        "date_range": "2023-01-01 to 2024-01-26",
        "success_rate": 0.68,
        "avg_return": 0.024,
        "avg_hold_time": "2.5 days",
        "win_rate": 0.68,
        "max_drawdown": -0.08
    },

    # Optimization suggestions
    "optimization_suggestions": [
        "Try gap_over_atr range 0.75-0.90 for higher win rate",
        "Consider tightening stop loss to 1.2R to reduce drawdown",
        "Best performance in volatile markets (VIX > 20)"
    ],

    # Recommended scanner
    "recommended_scanner": {
        "description": "Backside B scanner with A+ parameters",
        "scanner_code": "...",
        "expected_performance": {
            "win_rate": 0.70,
            "return": 0.025
        }
    }
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INVALID_INPUT | Neither image_url nor text_description provided | Need either image or text description |
| NO_SIMILAR_PATTERNS | Cannot find similar historical patterns | No historical matches for this setup |
| INSUFFICIENT_DATA | Not enough historical data | Need more historical data for validation |

#### Test Cases

```python
# Test 1: Image-based analysis
input1 = {
    "a_plus_example": {
        "image_url": "https://example.com/chart.png",
        "text_description": "Gap up into resistance",
        "date": "2024-01-26"
    },
    "validate_historical": True
}
# Expected: Setup detected with parameters

# Test 2: Text-based only
input2 = {
    "a_plus_example": {
        "text_description": "Backside euphoric top with gap up and red candle close at lows",
        "date": "2024-01-26"
    }
}
# Expected: Setup detected from description

# Test 3: No input
input3 = {
    "a_plus_example": {}
}
# Expected: INVALID_INPUT error

# Test 4: No historical matches
input4 = {
    "a_plus_example": {
        "text_description": "Very unique setup never seen before",
        "date": "2024-01-26"
    },
    "validate_historical": True
}
# Expected: NO_SIMILAR_PATTERNS warning
```

---

### TOOL 8: `quick_backtester`

**Version**: 1.0.0
**Purpose**: Fast 30-day backtest for quick validation
**Estimated LOC**: 90 lines

#### Input Specification

```python
{
    # Required
    "scanner_code": str,
    "start_date": str,
    "end_date": str,

    # Entry/Exit rules
    "entry_rules": {
        "conditions": ["gap_over_atr > 0.8"],
        "entry_time": "09:45",
        "entry_type": "MARKET"
    },
    "exit_rules": {
        "target_profit": 2.5,  # Risk multiple
        "stop_loss": 1.5,
        "max_hold_days": 5,
        "exit_time": "15:45"
    },

    # Position sizing
    "position_sizing": {
        "method": "FIXED",  # FIXED, VOLATILITY, PERCENT
        "account_size": 100000,
        "risk_per_trade": 0.01,
        "position_size": 100
    },

    # Options
    "include_commission": True,
    "commission_per_share": 0.005,
    "slippage": 0.01
}
```

#### Output Specification

```python
{
    "backtest_results": {
        # Summary stats
        "total_trades": 23,
        "winners": 16,
        "losers": 7,
        "win_rate": 0.696,

        # Performance
        "total_return": 0.084,  # 8.4%
        "sharpe_ratio": 1.85,
        "sortino_ratio": 2.12,
        "max_drawdown": -0.052,
        "avg_return_per_trade": 0.0037,

        # Trade breakdown
        "trades": [
            {
                "entry_date": "2024-01-10",
                "entry_price": 150.25,
                "exit_date": "2024-01-12",
                "exit_price": 154.50,
                "pnl": 0.028,  # 2.8%
                "hold_days": 2,
                "return_r": 2.8
            }
        ],

        # Equity curve
        "equity_curve": {
            "dates": ["2024-01-01", "2024-01-02", ...],
            "equity": [1.0, 1.02, 1.05, ...],
            "drawdowns": [0, 0, -0.02, ...]
        }
    },

    # Execution info
    "execution_time": 4.2,  # seconds
    "bars_analyzed": 500,
    "warnings": ["Low sample size - only 23 trades"]
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INSUFFICIENT_DATA | Not enough bars in date range | Need at least 20 bars of data |
| INVALID_DATES | end_date before start_date | Invalid date range |
| MISSING_COLUMNS | Scanner code doesn't return required fields | Scanner must return entry/exit signals |
| EXECUTION_FAILED | Backtest execution failed | Check scanner code and entry/exit rules |

#### Test Cases

```python
# Test 1: Successful backtest
input1 = {
    "scanner_code": scanner_code,
    "start_date": "2024-01-01",
    "end_date": "2024-01-30",
    "entry_rules": {"conditions": ["gap_over_atr > 0.8"]},
    "exit_rules": {"target_profit": 2.5, "stop_loss": 1.5}
}
# Expected: Backtest results with trades

# Test 2: Invalid date range
input2 = {
    "scanner_code": scanner_code,
    "start_date": "2024-01-30",
    "end_date": "2024-01-01",  # End before start
    "entry_rules": {},
    "exit_rules": {}
}
# Expected: INVALID_DATES error

# Test 3: No signals
input3 = {
    "scanner_code": very_strict_scanner,  # Won't find any signals
    "start_date": "2024-01-01",
    "end_date": "2024-01-30",
    "entry_rules": {},
    "exit_rules": {}
}
# Expected: 0 trades with warning

# Test 4: Missing scanner code
input4 = {
    "scanner_code": "",
    "start_date": "2024-01-01",
    "end_date": "2024-01-30",
    "entry_rules": {},
    "exit_rules": {}
}
# Expected: MISSING_PARAMETER error
```

---

### TOOL 9: `knowledge_base_search`

**Version**: 1.0.0
**Purpose**: Search Archon knowledge base for V31, Lingua, strategies
**Estimated LOC**: 60 lines

#### Input Specification

```python
{
    # Required
    "query": str,  # Search query
    "context": str,  # "generating scanner", "backtesting", etc.

    # Search options
    "max_results": 5,
    "search_type": "SEMANTIC",  # SEMANTIC, KEYWORD, HYBRID
    "date_range": {
        "start": "2020-01-01",  # Optional
        "end": "2024-01-26"
    },

    # Filters
    "categories": [],  # [V31, LINGUA, STRATEGIES, SCANNERS]
    "min_relevance_score": 0.5,

    # Output options
    "include_snippets": True,
    "return_sources": True
}
```

#### Output Specification

```python
{
    "query": "backside scanner parameters",
    "total_found": 12,

    "results": [
        {
            "rank": 1,
            "relevance_score": 0.92,
            "title": "Backside B Scanner (2024)",
            "type": "STRATEGY",
            "summary": "Gap up setup with 68% win rate, optimized for volatile markets...",
            "snippet": "def backside_scanner(df): return df[df['gap_over_atr'] > 0.85]...",
            "source": "archon://strategies/backside_b",
            "date": "2024-01-15",
            "metadata": {
                "performance": {
                    "win_rate": 0.68,
                    "total_return": 0.24
                },
                "parameters": {
                    "gap_over_atr": 0.85,
                    "vol_mult": 1.2
                }
            }
        },
        {
            "rank": 2,
            "relevance_score": 0.78,
            "title": "Gap Continuation Setup",
            "type": "STRATEGY",
            "summary": "Similar gap setup but for continuation patterns...",
            "source": "archon://strategies/gap_continuation"
        }
    ],

    "search_time": 0.8,  # seconds
    "warnings": ["Consider broader date range for more results"]
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| ARCHON_CONNECTION_FAILED | Cannot connect to Archon | Archon service is not responding |
| NO_RESULTS | Search returned no results | Try a different query or broader criteria |
| QUERY_TOO_BROAD | Query is too vague | Be more specific in your search |

#### Test Cases

```python
# Test 1: Successful search
input1 = {
    "query": "backside scanner parameters",
    "context": "generating scanner",
    "max_results": 5
}
# Expected: List of relevant results

# Test 2: No results
input2 = {
    "query": "very unique query never seen before",
    "context": "research",
    "max_results": 5
}
# Expected: Empty results with NO_RESULTS warning

# Test 3: Archon not available
input3 = {
    "query": "test",
    "context": "test",
    "archon_url": "http://localhost:9999"  # Wrong port
}
# Expected: ARCHON_CONNECTION_FAILED error

# Test 4: Broad query
input4 = {
    "query": "scanner",  # Too broad
    "context": "research",
    "max_results": 50
}
# Expected: QUERY_TOO_BROAD warning
```

---

### TOOL 10: `similar_strategy_finder`

**Version**: 1.0.0
**Purpose**: Find semantically similar strategies with performance data
**Estimated LOC**: 80 lines

#### Input Specification

```python
{
    # Required
    "strategy_description": str,
    "parameters": dict,

    # Comparison options
    "include_performance": True,
    "similarity_threshold": 0.5,  # Min similarity score
    "max_results": 5,

    # Analysis options
    "parameter_sensitivity": "AUTO",  # AUTO, HIGH, LOW
    "return_optimization_suggestions": True
}
```

#### Output Specification

```python
{
    "query_strategy": {
        "description": "gap up backside",
        "parameters": {"gap_over_atr": 0.8}
    },

    "similar_strategies": [
        {
            "name": "Backside B Scanner",
            "similarity_score": 0.89,
            "match_type": "HIGH",  # HIGH, MEDIUM, LOW

            # Performance comparison
            "performance": {
                "win_rate": 0.68,
                "total_return": 0.24,
                "sharpe_ratio": 1.5,
                "max_drawdown": -0.08
            },

            # Parameter comparison
            "parameter_comparison": {
                "gap_over_atr": {
                    "query": 0.8,
                    "similar": 0.85,
                    "difference": "Query uses tighter gap threshold"
                },
                "vol_mult": {
                    "query": null,  # Not specified
                    "similar": 1.2,
                    "difference": "Similar strategy uses vol_mult filter"
                }
            },

            # Key differences
            "key_differences": [
                "Uses vol_mult instead of fixed % for volatility filter",
                "Adds EMA9 confirmation requirement"
            ]
        }
    ],

    # Optimization suggestions
    "optimization_suggestions": [
        "Try gap_over_atr range 0.75-0.90 for higher win rate",
        "Consider adding volume confirmation (vol_mult > 1.0)",
        "Best performance in volatile markets (VIX > 20)"
    ],

    "warnings": ["Low sample size - consider more data"]
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| NO_SIMILAR_STRATEGIES | No strategies found with threshold | Try lowering similarity_threshold |
| INVALID_PARAMETERS | Parameter dict is empty | Need at least one parameter for comparison |

#### Test Cases

```python
# Test 1: Find similar strategies
input1 = {
    "strategy_description": "gap up backside",
    "parameters": {"gap_over_atr": 0.8},
    "include_performance": True
}
# Expected: List of similar backside strategies

# Test 2: No matches
input2 = {
    "strategy_description": "very unique strategy never seen before",
    "parameters": {"unique_param": 999},
    "similarity_threshold": 0.9  # Very high threshold
}
# Expected: NO_SIMILAR_STRATEGIES warning

# Test 3: Empty parameters
input3 = {
    "strategy_description": "test strategy",
    "parameters": {}  # Empty
}
# Expected: INVALID_PARAMETERS error
```

---

### TOOL 11: `parameter_optimizer`

**Version**: 1.0.0
**Purpose**: Grid search optimization for strategy parameters
**Estimated LOC**: 80 lines

#### Input Specification

```python
{
    # Required
    "scanner_code": str,
    "parameter_ranges": {
        "gap_over_atr": {
            "min": 0.7,
            "max": 1.2,
            "step": 0.05
        },
        "vol_mult": {
            "min": 1.0,
            "max": 1.5,
            "step": 0.1
        }
    },

    # Optimization settings
    "optimization_metric": "sharpe_ratio",  # sharpe_ratio, win_rate, total_return
    "max_iterations": 100,
    "backtest_period_days": 30,

    # Options
    "return_all_results": True,
    "early_stop": True,
    "early_stop_threshold": 0.9  # If score > 0.9, stop
}
```

#### Output Specification

```python
{
    "optimization_summary": {
        "total_iterations": 80,
        "best_sharpe_ratio": 2.1,
        "optimization_time": 45.2  # seconds
    },

    # Best parameters
    "best_parameters": {
        "gap_over_atr": 0.85,
        "vol_mult": 1.2
    },

    # Best performance
    "best_performance": {
        "sharpe_ratio": 2.1,
        "win_rate": 0.72,
        "total_return": 0.28,
        "max_drawdown": -0.06
    },

    # All results (top 10)
    "all_results": [
        {
            "rank": 1,
            "parameters": {"gap_over_atr": 0.85, "vol_mult": 1.2},
            "sharpe_ratio": 2.1,
            "win_rate": 0.72,
            "total_return": 0.28
        },
        {
            "rank": 2,
            "parameters": {"gap_over_atr": 0.80, "vol_mult": 1.1},
            "sharpe_ratio": 1.95,
            "win_rate": 0.68,
            "total_return": 0.24
        }
        # ... up to max_iterations
    ],

    # Parameter sensitivity
    "parameter_sensitivity": {
        "gap_over_atr": {
            "low": 0.75,
            "high": 0.95,
            "optimal": 0.85,
            "sensitivity": "MEDIUM"  # LOW, MEDIUM, HIGH
        },
        "vol_mult": {
            "low": 1.1,
            "high": 1.3,
            "optimal": 1.2,
            "sensitivity": "LOW"
        }
    }
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| NO_PROFITABLE_PARAMETERS | No profitable combinations found | All combinations produced losses |
| TIMEOUT | Optimization took too long | Partial results only |
| INSUFFICIENT_DATA | Not enough backtest data | Need more data for reliable optimization |

#### Test Cases

```python
# Test 1: Successful optimization
input1 = {
    "scanner_code": scanner_code,
    "parameter_ranges": {
        "gap_over_atr": {"min": 0.7, "max": 1.2, "step": 0.1}
    },
    "optimization_metric": "sharpe_ratio",
    "max_iterations": 50
}
# Expected: Best parameters found

# Test 2: No profitable results
input2 = {
    "scanner_code": bad_scanner,  # Loses money
    "parameter_ranges": {
        "gap_over_atr": {"min": 0.7, "max": 1.2, "step": 0.1}
    },
    "optimization_metric": "total_return",
    "max_iterations": 20
}
# Expected: NO_PROFITABLE_PARAMETERS warning

# Test 3: Timeout
input3 = {
    "scanner_code": complex_scanner,
    "parameter_ranges": large_range,
    "optimization_metric": "sharpe_ratio",
    "max_iterations": 10000,
    "timeout": 10
}
# Expected: TIMEOUT with partial results
```

---

### TOOL 12: `position_risk_calculator`

**Version**: 1.0.0
**Purpose**: Calculate position sizes, stop losses, and risk limits
**Estimated LOC**: 100 lines

#### Input Specification

```python
{
    # Required
    "account_size": float,
    "risk_per_trade": float,  # Percentage (0.01 = 1%)

    # Trade details
    "entry_price": float,
    "stop_distance": float,  # ATR-based or fixed amount

    # Calculation method
    "method": "VOLATILITY_BASED",  # VOLATILITY_BASED, FIXED, PERCENT, KELLY
    "atr": float,  # Required for VOLATILITY_BASED

    # Portfolio rules
    "portfolio_rules": {
        "max_positions": 10,
        "max_portfolio_risk": 0.05,  # 5% of account
        "daily_loss_limit": 0.02,  # 2% daily loss limit
        "current_positions": [...],
        "current_daily_pnl": -0.005  # Already down 0.5%
    },

    # Options
    "include_exit_levels": True,
    "target_profit_multiple": 2.5,
    "trailing_stop": True
}
```

#### Output Specification

```python
{
    "position_size": {
        "shares": 400,
        "dollars": 60000,
        "percent_of_account": 0.60  # 60%
    },

    "risk_analysis": {
        "risk_amount": 1000,  # Dollars
        "risk_percent": 0.01,  # 1% of account
        "stop_loss_price": 147.50,
        "stop_distance_dollars": 2.50,
        "stop_distance_atr": 1.25
    },

    "exit_levels": {
        "take_profit_price": 155.00,
        "take_profit_dollars": 5.00,
        "risk_reward_ratio": 2.5,
        "trailing_stop": {
            "activate_at": 1.5,  # Trail after 1.5R profit
            "trail_distance": 1.5  # Trail by 1.5x ATR
        }
    },

    "portfolio_checks": {
        "within_position_limit": True,
        "within_portfolio_risk": True,
        "daily_loss_available": 800.0,  # $800 remaining today
        "can_trade": True
    },

    "recommendations": [
        "Position size is appropriate",
        "Consider reducing size if daily loss limit hit"
    ],

    "warnings": ["High correlation with existing positions"]
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| INSUFFICIENT_FUNDS | Account size too small for position | Need minimum account size |
| RISK_TOO_HIGH | Risk per trade exceeds recommended | Keep risk under 2% per trade |
| DAILY_LIMIT_HIT | Daily loss limit reached | Stop trading for today |

#### Test Cases

```python
# Test 1: Volatility-based position sizing
input1 = {
    "account_size": 100000,
    "risk_per_trade": 0.01,
    "entry_price": 150.00,
    "stop_distance": 2.50,
    "method": "VOLATILITY_BASED",
    "atr": 2.00
}
# Expected: Position size calculated based on ATR

# Test 2: Daily limit hit
input2 = {
    "account_size": 100000,
    "risk_per_trade": 0.01,
    "entry_price": 150.00,
    "stop_distance": 2.50,
    "method": "VOLATILITY_BASED",
    "atr": 2.00,
    "portfolio_rules": {
        "daily_loss_limit": 0.02,
        "current_daily_pnl": -0.019  # Already down 1.9%
    }
}
# Expected: DAILY_LIMIT_HIT warning

# Test 3: Risk too high
input3 = {
    "account_size": 100000,
    "risk_per_trade": 0.05,  # 5% risk (too high)
    "entry_price": 150.00,
    "stop_distance": 2.50,
    "method": "VOLATILITY_BASED",
    "atr": 2.00
}
# Expected: RISK_TOO_HIGH warning
```

---

### TOOL 13: `build_plan_generator`

**Version**: 1.0.0
**Purpose**: Create build plans from requirements
**Estimated LOC**: 60 lines

#### Input Specification

```python
{
    # Required
    "user_requirements": str,  # Natural language requirements

    # Optional A+ example
    "a_plus_example": {
        "text_description": str,
        "parameters": dict,
        "date": str
    },

    # Optional parameters
    "parameters": dict,

    # Plan options
    "include_testing": True,
    "include_backtesting": True,
    "include_execution": False,  # Not needed for scanner
    "include_risk_management": False,

    # Approval
    "require_approval": True
}
```

#### Output Specification

```python
{
    "plan_id": "plan_12345",
    "plan_name": "Backside B Scanner Build Plan",
    "created_date": "2024-01-26",

    "requirements_summary": {
        "description": "Build backside scanner for gap ups",
        "estimated_complexity": "MEDIUM",
        "estimated_time": "25 minutes"
    },

    # Build phases
    "phases": [
        {
            "phase_id": "phase_1",
            "name": "Generate V31 Scanner",
            "tool": "v31_scanner_generator",
            "description": "Generate V31-compliant scanner from requirements",
            "estimated_time": "15 min",
            "dependencies": [],
            "inputs": {
                "description": "Backside scanner for gap ups",
                "parameters": {"gap_over_atr": 0.8}
            },
            "outputs": {
                "scanner_code": "...",
                "validation_report": "..."
            }
        },
        {
            "phase_id": "phase_2",
            "name": "Validate V31 Compliance",
            "tool": "v31_validator",
            "description": "Validate scanner against V31 Gold Standard",
            "estimated_time": "5 min",
            "dependencies": ["phase_1"],
            "inputs": {
                "scanner_code": "from phase_1"
            },
            "outputs": {
                "validation_report": "..."
            }
        },
        {
            "phase_id": "phase_3",
            "name": "Quick Backtest",
            "tool": "quick_backtester",
            "description": "Run 30-day backtest for validation",
            "estimated_time": "5 min",
            "dependencies": ["phase_2"],
            "inputs": {
                "scanner_code": "from phase_1",
                "backtest_period": "2024-01-01 to 2024-01-30"
            },
            "outputs": {
                "backtest_results": "..."
            }
        }
    ],

    # Summary
    "total_phases": 3,
    "total_estimated_time": "25 minutes",
    "critical_path": "phase_1 → phase_2 → phase_3",

    # Approval
    "approval_required": True,
    "approval_status": "PENDING",
    "approved_by": None,
    "approval_date": None
}
```

#### Error Conditions

| Error Code | Condition | Message |
|-----------|-----------|---------|
| REQUIREMENTS_TOO_VAGUE | Cannot understand requirements | Please provide more details about what you want to build |
| MISSING_DEPENDENCY | Required dependency not available | Need to complete prerequisite first |

#### Test Cases

```python
# Test 1: Generate plan with A+ example
input1 = {
    "user_requirements": "Build backside scanner like this A+ example",
    "a_plus_example": {
        "text_description": "Gap up into resistance",
        "parameters": {"gap_over_atr": 0.85}
    },
    "include_testing": True
}
# Expected: 3-phase plan with testing

# Test 2: Vague requirements
input2 = {
    "user_requirements": "build me something good"
}
# Expected: REQUIREMENTS_TOO_VAGUE error

# Test 3: Without testing
input3 = {
    "user_requirements": "Build backside scanner",
    "include_testing": False
}
# Expected: 2-phase plan (no backtest phase)
```

---

## 🧪 TESTING FRAMEWORK

### Standard Test Structure

```python
import pytest
from tool_name import tool_function

class TestToolName:
    def setup_method(self):
        """Setup test data"""
        self.valid_input = {...}
        self.invalid_input = {...}

    def test_success_case(self):
        """Test normal operation"""
        result = tool_function(self.valid_input)
        assert result.status == ToolStatus.SUCCESS
        assert result.result is not None
        assert result.execution_time < 2.0

    def test_invalid_input(self):
        """Test error handling"""
        result = tool_function(self.invalid_input)
        assert result.status == ToolStatus.ERROR
        assert result.error is not None

    def test_performance(self):
        """Test execution time"""
        import time
        start = time.time()
        result = tool_function(self.valid_input)
        elapsed = time.time() - start
        assert elapsed < 2.0  # 2 second max for most tools

    def test_output_format(self):
        """Test output matches schema"""
        result = tool_function(self.valid_input)
        # Validate output against schema
        assert validate_output_schema(result.result)
```

### Test Coverage Requirements

- **Unit Tests**: 95%+ coverage per tool
- **Integration Tests**: Test tool combinations
- **Performance Tests**: Validate execution times
- **Error Handling Tests**: Test all error codes

---

## ⚡ PERFORMANCE BENCHMARKS

### Target Performance

| Tool | Target Time | Max Time |
|------|-------------|----------|
| `v31_scanner_generator` | <2s | 5s |
| `v31_validator` | <1s | 2s |
| `scanner_executor` | N/A | 300s timeout |
| `indicator_calculator` | <0.5s | 1s |
| `market_structure_analyzer` | <1s | 2s |
| `daily_context_detector` | <0.5s | 1s |
| `a_plus_analyzer` | <2s | 5s |
| `quick_backtester` | <5s | 30s |
| `knowledge_base_search` | <2s | 5s |
| `similar_strategy_finder` | <1s | 3s |
| `parameter_optimizer` | N/A | 60s timeout |
| `position_risk_calculator` | <0.1s | 0.5s |
| `build_plan_generator` | <0.5s | 2s |

### Performance Testing Template

```python
def benchmark_tool(tool_function, input_data, iterations=100):
    """
    Benchmark tool performance
    """
    import time

    times = []
    for _ in range(iterations):
        start = time.time()
        result = tool_function(input_data)
        elapsed = time.time() - start
        times.append(elapsed)

    return {
        "mean": np.mean(times),
        "median": np.median(times),
        "p95": np.percentile(times, 95),
        "p99": np.percentile(times, 99),
        "min": np.min(times),
        "max": np.max(times)
    }
```

---

## 📊 IMPLEMENTATION CHECKLIST

For each tool, verify before implementation:

- [ ] **Interface Defined**: Input/output specs complete
- [ ] **Error Handling**: All error codes defined
- [ ] **Test Cases**: Unit test cases written
- [ ] **Performance Target**: Execution time target set
- [ ] **Dependencies**: External dependencies identified
- [ ] **Documentation**: Docstrings complete

---

## ✅ TASK 1.3 COMPLETE

**All 13 tools fully specified with:**
- ✅ Detailed input/output specifications
- ✅ Complete error handling
- ✅ Test cases for each tool
- ✅ Performance benchmarks
- ✅ Ready for implementation

**Total Specification Pages**: 50+ pages of detailed specs

**Next Phase**: Task 2.1 - Implement Core Scanner Tools

---

**Tool Interfaces Completed**: January 26, 2026
**Ready for Implementation**: Task 2.1 (Week 1, Day 3)
**Owner**: CE-Hub Orchestrator

**All 13 tools ready for implementation!** 🎯
