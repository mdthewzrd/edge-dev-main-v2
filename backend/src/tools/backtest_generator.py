"""
Backtest Generator Tool

Purpose: Generate backtest code from scanner definition
Version: 1.0.0
Estimated LOC: 100 lines
Target Execution: <0.5 seconds

This tool does ONE thing: Generate backtest code from scanner.
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


def backtest_generator(input_data: Dict[str, Any]) -> ToolResult:
    """
    Generate backtest code from scanner definition

    Creates a complete backtest script based on scanner parameters
    and backtest configuration.

    Args:
        input_data: Dictionary with:
            - scanner_code (str): V31 scanner code [REQUIRED]
            - backtest_config (dict): Backtest configuration [REQUIRED]
            - output_format (str): Output format (default: 'python')
            - include_comments (bool): Add explanatory comments (default: True)
            - include_visualization (bool): Add visualization code (default: False)

    Returns:
        ToolResult with generated backtest code
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
        scanner_code = input_data.get("scanner_code", "")
        backtest_config = input_data.get("backtest_config", {})
        output_format = input_data.get("output_format", "python")
        include_comments = input_data.get("include_comments", True)
        include_visualization = input_data.get("include_visualization", False)

        # Extract scanner parameters
        scanner_params = extract_scanner_parameters(scanner_code)

        # Generate backtest code
        backtest_code = generate_backtest_code(
            scanner_code,
            scanner_params,
            backtest_config,
            include_comments,
            include_visualization
        )

        # Calculate code statistics
        code_stats = calculate_code_stats(backtest_code)

        # Prepare result
        result = {
            "backtest_code": backtest_code,
            "format": output_format,
            "scanner_parameters": scanner_params,
            "backtest_config": backtest_config,
            "code_stats": code_stats
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

    # Check required fields
    required_fields = ["scanner_code", "backtest_config"]
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

    # Validate scanner_code
    scanner_code = input_data.get("scanner_code", "")
    if not scanner_code or not isinstance(scanner_code, str):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "scanner_code must be a non-empty string",
                "parameter": "scanner_code"
            }
        }

    # Validate backtest_config
    backtest_config = input_data.get("backtest_config", {})
    if not isinstance(backtest_config, dict):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "backtest_config must be a dictionary",
                "parameter": "backtest_config"
            }
        }

    return {"valid": True}


def extract_scanner_parameters(scanner_code: str) -> Dict[str, Any]:
    """
    Extract parameters from scanner code

    Returns:
        Dictionary with extracted parameters
    """

    # This is a simplified implementation
    # In production, you'd use AST parsing for accurate extraction

    params = {
        "setup_types": [],
        "indicators": [],
        "filters": []
    }

    # Detect setup types
    if "backside" in scanner_code.lower():
        params["setup_types"].append("BACKSIDE_B")
    if "d2" in scanner_code.lower() or "continuation" in scanner_code.lower():
        params["setup_types"].append("D2")
    if "mdr" in scanner_code.lower() or "multi" in scanner_code.lower():
        params["setup_types"].append("MDR")

    # Detect indicators
    if "ema" in scanner_code.lower():
        params["indicators"].append("EMA")
    if "atr" in scanner_code.lower():
        params["indicators"].append("ATR")
    if "volume" in scanner_code.lower():
        params["indicators"].append("Volume")
    if "rsi" in scanner_code.lower():
        params["indicators"].append("RSI")

    # Detect filters
    if "gap" in scanner_code.lower():
        params["filters"].append("gap_filter")
    if "stage1" in scanner_code.lower() or "get_stage1" in scanner_code.lower():
        params["filters"].append("market_universe_filter")

    return params


def generate_backtest_code(
    scanner_code: str,
    scanner_params: Dict[str, Any],
    backtest_config: Dict[str, Any],
    include_comments: bool,
    include_visualization: bool
) -> str:

    """
    Generate backtest code

    Returns:
        Generated backtest code string
    """

    # Extract backtest parameters
    start_date = backtest_config.get("start_date", "2023-01-01")
    end_date = backtest_config.get("end_date", "2024-01-01")
    initial_capital = backtest_config.get("initial_capital", 100000)
    position_size = backtest_config.get("position_size", 0.02)
    max_positions = backtest_config.get("max_positions", 10)

    # Generate code
    code_lines = []

    if include_comments:
        code_lines.append('#"')
        code_lines.append('# Backtest Script Generated by RENATA V2')
        code_lines.append('#')
        code_lines.append(f'# Scanner Parameters: {scanner_params["setup_types"]}')
        code_lines.append(f'# Backtest Period: {start_date} to {end_date}')
        code_lines.append(f'# Initial Capital: ${initial_capital:,.0f}')
        code_lines.append('#"')
        code_lines.append('')

    # Imports
    code_lines.append('import pandas as pd')
    code_lines.append('import numpy as np')
    code_lines.append('from datetime import datetime')
    code_lines.append('')

    # Scanner code
    if include_comments:
        code_lines.append('# Scanner Code')
    code_lines.append(scanner_code)
    code_lines.append('')

    # Backtest configuration
    if include_comments:
        code_lines.append('# Backtest Configuration')
    code_lines.append(f'START_DATE = "{start_date}"')
    code_lines.append(f'END_DATE = "{end_date}"')
    code_lines.append(f'INITIAL_CAPITAL = {initial_capital}')
    code_lines.append(f'POSITION_SIZE = {position_size}')
    code_lines.append(f'MAX_POSITIONS = {max_positions}')
    code_lines.append('')

    # Backtest execution
    if include_comments:
        code_lines.append('# Backtest Execution')
    code_lines.append('def run_backtest():')
    code_lines.append('    """Run backtest with scanner"""')
    code_lines.append('')
    code_lines.append('    # Load historical data')
    code_lines.append('    data = load_market_data(START_DATE, END_DATE)')
    code_lines.append('')
    code_lines.append('    # Run scanner')
    code_lines.append('    signals = stage2_process_symbols(data)')
    code_lines.append('')
    code_lines.append('    # Calculate returns')
    code_lines.append('    returns = calculate_returns(signals, POSITION_SIZE)')
    code_lines.append('')
    code_lines.append('    # Calculate metrics')
    code_lines.append('    metrics = calculate_performance_metrics(returns, INITIAL_CAPITAL)')
    code_lines.append('')
    code_lines.append('    return metrics')
    code_lines.append('')
    code_lines.append('')
    code_lines.append('def calculate_returns(signals, position_size):')
    code_lines.append('    """Calculate returns for each signal"""')
    code_lines.append('    returns = []')
    code_lines.append('    for signal in signals:')
    code_lines.append('        entry_price = signal["entry_price"]')
    code_lines.append('        exit_price = signal["exit_price"]')
    code_lines.append('        position_return = (exit_price - entry_price) / entry_price')
    code_lines.append('        returns.append({')
    code_lines.append('            "ticker": signal["ticker"],')
    code_lines.append('            "entry_price": entry_price,')
    code_lines.append('            "exit_price": exit_price,')
    code_lines.append('            "return": position_return,')
    code_lines.append('            "position_size": position_size')
    code_lines.append('        })')
    code_lines.append('    return pd.DataFrame(returns)')
    code_lines.append('')
    code_lines.append('')
    code_lines.append('def calculate_performance_metrics(returns, initial_capital):')
    code_lines.append('    """Calculate performance metrics"""')
    code_lines.append('    total_return = returns["return"].sum()')
    code_lines.append('    win_rate = (returns["return"] > 0).sum() / len(returns)')
    code_lines.append('    sharpe_ratio = returns["return"].mean() / returns["return"].std()')
    code_lines.append('')
    code_lines.append('    final_capital = initial_capital * (1 + total_return)')
    code_lines.append('')
    code_lines.append('    return {')
    code_lines.append('        "total_return": total_return,')
    code_lines.append('        "win_rate": win_rate,')
    code_lines.append('        "sharpe_ratio": sharpe_ratio,')
    code_lines.append('        "final_capital": final_capital,')
    code_lines.append('        "num_trades": len(returns)')
    code_lines.append('    }')
    code_lines.append('')
    code_lines.append('')
    code_lines.append('if __name__ == "__main__":')
    code_lines.append('    metrics = run_backtest()')
    code_lines.append('    print(f"Total Return: {metrics["total_return"]:.2%}")')
    code_lines.append('    print(f"Win Rate: {metrics["win_rate"]:.2%}")')
    code_lines.append('    print(f"Sharpe Ratio: {metrics["sharpe_ratio"]:.2f}")')
    code_lines.append('    print(f"Final Capital: ${metrics["final_capital"]:,.2f}")')

    # Add visualization if requested
    if include_visualization:
        code_lines.append('')
        code_lines.append('')
        if include_comments:
            code_lines.append('# Visualization')
        code_lines.append('import matplotlib.pyplot as plt')
        code_lines.append('')
        code_lines.append('def plot_equity_curve(returns, initial_capital):')
        code_lines.append('    """Plot equity curve"""')
        code_lines.append('    cumulative_returns = (1 + returns["return"]).cumprod()')
        code_lines.append('    equity = initial_capital * cumulative_returns')
        code_lines.append('')
        code_lines.append('    plt.figure(figsize=(12, 6))')
        code_lines.append('    plt.plot(equity)')
        code_lines.append('    plt.title("Equity Curve")')
        code_lines.append('    plt.xlabel("Trade Number")')
        code_lines.append('    plt.ylabel("Portfolio Value")')
        code_lines.append('    plt.grid(True)')
        code_lines.append('    plt.show()')

    return "\n".join(code_lines)


def calculate_code_stats(code: str) -> Dict[str, Any]:
    """
    Calculate code statistics

    Returns:
        Dictionary with code statistics
    """

    lines = code.split("\n")
    non_empty_lines = [l for l in lines if l.strip()]

    return {
        "total_lines": len(lines),
        "code_lines": len(non_empty_lines),
        "comment_lines": len([l for l in lines if l.strip().startswith("#")]),
        "blank_lines": len([l for l in lines if not l.strip()]),
        "estimated_chars": len(code)
    }


if __name__ == "__main__":
    # Test the tool
    sample_scanner = """
def stage2_process_symbols(df):
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

    backtest_config = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "initial_capital": 100000,
        "position_size": 0.02,
        "max_positions": 10
    }

    test_input = {
        "scanner_code": sample_scanner,
        "backtest_config": backtest_config,
        "include_comments": True,
        "include_visualization": True
    }

    result = backtest_generator(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Backtest code generated successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Code Lines: {result.result['code_stats']['total_lines']}")
        print(f"Code Chars: {result.result['code_stats']['estimated_chars']}")
        print(f"\nGenerated Code (first 500 chars):")
        print(result.result['backtest_code'][:500] + "...")
    else:
        print(f"❌ Error: {result.error}")
