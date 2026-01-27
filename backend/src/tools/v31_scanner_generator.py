"""
V31 Scanner Generator Tool

Purpose: Generate V31-compliant scanner code from natural language or A+ examples
Version: 1.0.0
Estimated LOC: 150 lines
Target Execution: <2 seconds

This tool does ONE thing: Convert descriptions/A+ examples into V31 scanner code.
"""

import re
from typing import Dict, Any, Optional, List
import time

# Import shared types - handle both relative and absolute imports
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


# V31 Scanner Templates
V31_TEMPLATES = {
    "backside_b": """
# V31 Scanner: Backside B Setup
# Generated: {timestamp}
# Description: {description}

import pandas as pd
import numpy as np

# ====================
# PARAMETERS
# ====================
{parameters}

# ====================
# STAGE 1: MARKET SCANNING
# ====================
def get_stage1_symbols():
    \"\"\"Fetch all symbols for market scanning\"\"\"
    # Return full market universe (12k+ tickers)
    # This is optimized via grouped API endpoints
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

    # EMA9 for trend reference
    df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()

    # Gap detection
    df['gap'] = df['open'] - df['close'].shift(1)
    df['gap_over_atr'] = df['gap'] / df['atr']

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
    \"\"\"

    # Filter 1: Minimum price
    if df['close'].iloc[-1] < 10:
        return False

    # Filter 2: Minimum volume
    if df['volume'].iloc[-1] < 1000000:
        return False

    # Filter 3: Has gap
    if df['gap_over_atr'].iloc[-1] < gap_over_atr_min:
        return False

    return True

def detect_setup(df: pd.DataFrame) -> pd.DataFrame:
    \"\"\"
    Detect Backside B setup (Stage 2.3)
    Returns DataFrame with signal details
    \"\"\"

    # Get latest data
    latest = df.iloc[-1]

    # Condition 1: Gap up over ATR
    gap_condition = latest['gap_over_atr'] >= gap_over_atr_min

    # Condition 2: Open below EMA9 (backside)
    open_condition = latest['open'] < latest['ema9'] * open_over_ema9_min

    # Condition 3: Red candle close
    close_condition = latest['close'] < latest['open']

    if all([gap_condition, open_condition, close_condition]):
        # Signal found!
        signal_df = pd.DataFrame({{
            'ticker': df.name if hasattr(df, 'name') else 'UNKNOWN',
            'signal_time': df.index[-1],
            'entry_price': latest['close'],
            'gap_size': latest['gap_over_atr'],
            'open_vs_ema9': latest['open'] / latest['ema9'],
            'confidence': 0.75
        }})

        return signal_df

    return pd.DataFrame()  # No signal

# ====================
# STAGE 3: AGGREGATION
# ====================
def aggregate_signals(all_signals: List[pd.DataFrame]) -> pd.DataFrame:
    \"\"\"
    Aggregate signals from all tickers
    Apply final ranking and filtering
    \"\"\"

    if not all_signals:
        return pd.DataFrame()

    # Combine all signals
    combined = pd.concat(all_signals, ignore_index=True)

    # Sort by confidence
    combined = combined.sort_values('confidence', ascending=False)

    return combined
""",
}


def v31_scanner_generator(input_data: Dict[str, Any]) -> ToolResult:
    """
    Generate V31-compliant scanner code from description or A+ example

    Args:
        input_data: Dictionary with:
            - description (str): Natural language description [REQUIRED]
            - a_plus_example (dict, optional): A+ example with parameters
            - parameters (dict, optional): Parameter ranges
            - include_comments (bool): Add explanatory comments
            - include_validation (bool): Run v31_validator after generation
            - output_format (str): python, json

    Returns:
        ToolResult with scanner_code, validation_report, metadata
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
        description = input_data.get("description", "")
        a_plus_example = input_data.get("a_plus_example", {})
        parameters = input_data.get("parameters", {})
        include_comments = input_data.get("include_comments", True)
        include_validation = input_data.get("include_validation", True)

        # Determine scanner type from description
        scanner_type = detect_scanner_type(description, a_plus_example)

        # Get parameters (use A+ example if provided, otherwise use defaults)
        scanner_params = extract_parameters(scanner_type, a_plus_example, parameters)

        # Generate code from template
        scanner_code = generate_code_from_template(
            scanner_type=scanner_type,
            description=description,
            parameters=scanner_params,
            include_comments=include_comments
        )

        # Validate code structure
        code_structure = validate_code_structure(scanner_code)

        # Run V31 validation if requested
        validation_report = None
        v31_validated = False
        validation_warnings = []

        if include_validation:
            try:
                # Import here to avoid circular dependency
                # Try absolute import first, then relative import
                try:
                    from tools.v31_validator import v31_validator as validator
                except ImportError:
                    from .v31_validator import v31_validator as validator

                validation_result = validator({
                    "scanner_code": scanner_code,
                    "strict_mode": False,
                    "return_fixes": True
                })

                validation_report = validation_result.result
                v31_validated = validation_report.get("is_v31_compliant", False)
            except Exception as e:
                # Validation failed - continue without it
                validation_warnings.append(f"V31 validation failed: {str(e)}")

        # Calculate metadata
        result = {
            "scanner_code": scanner_code,
            "code_structure": code_structure,
            "v31_validated": v31_validated,
            "validation_report": validation_report,
            "parameters_used": scanner_params,
            "estimated_execution_time": estimate_execution_time(scanner_type),
            "estimated_signals": estimate_signal_count(scanner_type),
            "warnings": validation_warnings
        }

        return ToolResult(
            status=ToolStatus.SUCCESS,
            result=result,
            error=None,
            warnings=result.get("warnings", []),
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
    if "description" not in input_data or not input_data["description"].strip():
        return {
            "valid": False,
            "error": {
                "code": "MISSING_PARAMETER",
                "message": "Required parameter 'description' is missing or empty",
                "parameter": "description",
                "expected_type": "str",
                "suggestion": "Provide a clear description of the scanner you want to generate"
            }
        }

    # Check description length
    description = input_data["description"]
    if len(description) < 10:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "Description is too vague",
                "parameter": "description",
                "min_length": 10,
                "suggestion": "Please provide more details about the scanner (setup type, conditions, etc.)"
            }
        }

    return {"valid": True}


def detect_scanner_type(description: str, a_plus_example: Dict) -> str:
    """
    Detect scanner type from description or A+ example

    Returns:
        Scanner type key for template lookup
    """

    description_lower = description.lower()

    # Check for backside patterns
    if any(keyword in description_lower for keyword in ["backside", "gap up into resistance", "red candle"]):
        return "backside_b"

    # Check A+ example for hints
    if a_plus_example:
        params = a_plus_example.get("parameters", {})
        if "gap_over_atr" in params:
            return "backside_b"

    # Default: use backside_b as example template
    return "backside_b"


def extract_parameters(scanner_type: str, a_plus_example: Dict, user_params: Dict) -> Dict[str, Any]:
    """
    Extract and merge parameters from A+ example and user input

    Returns:
        Dictionary of parameters with min/max/default values
    """

    # Default parameters for backside_b
    default_params = {
        "gap_over_atr": {"min": 0.8, "max": 1.2, "default": 1.0},
        "open_over_ema9": {"min": 0.85, "max": 0.98, "default": 0.92},
    }

    # Override with A+ example parameters
    if a_plus_example and "parameters" in a_plus_example:
        for key, value in a_plus_example["parameters"].items():
            if key in default_params:
                default_params[key]["default"] = value

    # Override with user-provided parameter ranges
    if user_params:
        for key, value in user_params.items():
            if key in default_params:
                default_params[key].update(value)

    return default_params


def generate_code_from_template(
    scanner_type: str,
    description: str,
    parameters: Dict[str, Any],
    include_comments: bool
) -> str:
    """
    Generate scanner code from template

    Args:
        scanner_type: Type of scanner
        description: Natural language description
        parameters: Parameter definitions
        include_comments: Whether to include explanatory comments

    Returns:
        Complete V31 scanner code as string
    """

    # Get template
    template = V31_TEMPLATES.get(scanner_type, V31_TEMPLATES["backside_b"])

    # Format parameters section
    params_section = format_parameters(parameters)

    # Generate code
    from datetime import datetime
    scanner_code = template.format(
        timestamp=datetime.now().isoformat(),
        description=description,
        parameters=params_section
    )

    return scanner_code


def format_parameters(parameters: Dict[str, Any]) -> str:
    """Format parameters for code generation"""

    lines = []
    for param_name, param_def in parameters.items():
        default_val = param_def.get("default", 1.0)
        min_val = param_def.get("min", default_val * 0.8)
        max_val = param_def.get("max", default_val * 1.2)

        lines.append(f"# {param_name}: range {min_val}-{max_val}")
        lines.append(f"{param_name}_min = {min_val}")
        lines.append(f"{param_name}_max = {max_val}")
        lines.append(f"{param_name}_default = {default_val}")
        lines.append("")

    return "\n".join(lines)


def validate_code_structure(scanner_code: str) -> Dict[str, bool]:
    """
    Validate that generated code has required V31 structure elements

    Returns:
        Dict with structure validation results
    """

    structure_checks = {
        "has_stage1": "def get_stage1_symbols" in scanner_code,
        "has_stage2": "def stage2_process_symbols" in scanner_code,
        "has_stage3": "def aggregate_signals" in scanner_code,
        "per_ticker_operations": "def calculate_indicators" in scanner_code,
        "smart_filters": "def passes_smart_filters" in scanner_code,
    }

    return structure_checks


def estimate_execution_time(scanner_type: str) -> str:
    """Estimate execution time for generated scanner"""

    estimates = {
        "backside_b": "3 minutes for 5000 symbols",
    }

    return estimates.get(scanner_type, "5 minutes for 5000 symbols")


def estimate_signal_count(scanner_type: str) -> int:
    """Estimate expected signal count"""

    estimates = {
        "backside_b": 50,  # ~1% of 5000 symbols
    }

    return estimates.get(scanner_type, 30)


if __name__ == "__main__":
    # Test the tool
    test_input = {
        "description": "Backside scanner for gap ups with ATR filter",
        "parameters": {
            "gap_over_atr": {"min": 0.8, "max": 1.2, "default": 1.0}
        },
        "include_comments": True,
        "include_validation": False  # Skip for standalone test
    }

    result = v31_scanner_generator(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Scanner generated successfully!")
        print(f"Execution time: {result.execution_time:.3f}s")
        print(f"\nGenerated code:\n{result.result['scanner_code'][:500]}...")
    else:
        print(f"❌ Error: {result.error}")
