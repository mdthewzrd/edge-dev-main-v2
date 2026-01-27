"""
Quick Backtester Tool

Purpose: Fast 30-day backtest validation for scanners
Version: 1.0.0
Estimated LOC: 90 lines
Target Execution: <2 seconds

This tool does ONE thing: Run quick backtest on last 30 days of data.
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


def quick_backtester(input_data: Dict[str, Any]) -> ToolResult:
    """
    Run fast 30-day backtest validation

    Provides quick validation of scanner performance over the last 30 days.
    This is NOT a full backtest - it's a validation sanity check.

    Args:
        input_data: Dictionary with:
            - scanner_results (pd.DataFrame): Scanner execution results [REQUIRED]
            - entry_price_col (str): Column name for entry price (default: 'entry_price')
            - exit_price_col (str): Column name for exit price (default: 'exit_price')
            - date_col (str): Column name for date (default: 'date')
            - return_trades (bool): Include individual trade details (default: True)
            - benchmark_return (float): Benchmark return for comparison (default: 0.02)

    Returns:
        ToolResult with backtest validation metrics
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
        scanner_results = input_data.get("scanner_results")
        entry_price_col = input_data.get("entry_price_col", "entry_price")
        exit_price_col = input_data.get("exit_price_col", "exit_price")
        date_col = input_data.get("date_col", "date")
        return_trades = input_data.get("return_trades", True)
        benchmark_return = input_data.get("benchmark_return", 0.02)

        # Calculate metrics
        metrics = calculate_backtest_metrics(
            scanner_results,
            entry_price_col,
            exit_price_col,
            date_col,
            benchmark_return
        )

        # Analyze trade distribution
        trade_analysis = analyze_trade_distribution(
            scanner_results,
            entry_price_col,
            exit_price_col
        )

        # Prepare individual trades if requested
        trades_detail = []
        if return_trades and not scanner_results.empty:
            trades_detail = prepare_trade_details(
                scanner_results,
                entry_price_col,
                exit_price_col,
                date_col
            )

        # Determine validation result
        validation_passed = metrics["total_return"] >= 0 and metrics["win_rate"] >= 0.4

        # Prepare result
        result = {
            "validation_passed": validation_passed,
            "period_days": 30,
            "total_trades": metrics["total_trades"],
            "winning_trades": metrics["winning_trades"],
            "losing_trades": metrics["losing_trades"],
            "win_rate": round(metrics["win_rate"], 3),
            "total_return": round(metrics["total_return"], 3),
            "avg_return_per_trade": round(metrics["avg_return"], 3),
            "best_trade": round(metrics["best_trade"], 3),
            "worst_trade": round(metrics["worst_trade"], 3),
            "sharpe_ratio": round(metrics["sharpe_ratio"], 2),
            "benchmark_return": benchmark_return,
            "vs_benchmark": round(metrics["total_return"] - benchmark_return, 3),
            "trade_analysis": trade_analysis,
            "trades_detail": trades_detail
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
    required_fields = ["scanner_results"]
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

    # Validate scanner_results
    scanner_results = input_data.get("scanner_results")
    if scanner_results is None:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "scanner_results cannot be None",
                "parameter": "scanner_results"
            }
        }

    # Check if it's a DataFrame
    if not isinstance(scanner_results, pd.DataFrame):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "scanner_results must be a pandas DataFrame",
                "parameter": "scanner_results"
            }
        }

    # Check for data FIRST (before checking columns)
    if len(scanner_results) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INSUFFICIENT_DATA",
                "message": "scanner_results is empty",
                "minimum_required": 1
            }
        }

    # Check for required columns
    entry_col = input_data.get("entry_price_col", "entry_price")
    exit_col = input_data.get("exit_price_col", "exit_price")

    required_cols = [entry_col, exit_col]
    missing_cols = [col for col in required_cols if col not in scanner_results.columns]

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

    return {"valid": True}


def calculate_backtest_metrics(
    df: pd.DataFrame,
    entry_col: str,
    exit_col: str,
    date_col: str,
    benchmark_return: float
) -> Dict[str, Any]:

    """
    Calculate backtest performance metrics

    Returns:
        Dictionary with performance metrics
    """

    # Calculate returns for each trade
    df = df.copy()
    df['return'] = (df[exit_col] - df[entry_col]) / df[entry_col]

    # Basic metrics
    total_trades = len(df)
    winning_trades = len(df[df['return'] > 0])
    losing_trades = len(df[df['return'] <= 0])

    win_rate = winning_trades / total_trades if total_trades > 0 else 0.0

    # Return metrics
    total_return = df['return'].sum()
    avg_return = df['return'].mean()

    # Best/worst trades
    best_trade = df['return'].max() if total_trades > 0 else 0.0
    worst_trade = df['return'].min() if total_trades > 0 else 0.0

    # Calculate Sharpe ratio (simplified)
    if total_trades > 1:
        returns_std = df['return'].std()
        sharpe_ratio = (avg_return / returns_std) if returns_std > 0 else 0.0
    else:
        sharpe_ratio = 0.0

    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "total_return": total_return,
        "avg_return": avg_return,
        "best_trade": best_trade,
        "worst_trade": worst_trade,
        "sharpe_ratio": sharpe_ratio
    }


def analyze_trade_distribution(
    df: pd.DataFrame,
    entry_col: str,
    exit_col: str
) -> Dict[str, Any]:

    """
    Analyze trade distribution patterns

    Returns:
        Dictionary with distribution analysis
    """

    df = df.copy()
    df['return'] = (df[exit_col] - df[entry_col]) / df[entry_col]

    # Return buckets
    buckets = {
        "large_losses": len(df[df['return'] < -0.05]),  # >5% loss
        "small_losses": len(df[(df['return'] >= -0.05) & (df['return'] < 0)]),
        "small_gains": len(df[(df['return'] >= 0) & (df['return'] <= 0.05)]),
        "large_gains": len(df[df['return'] > 0.05])  # >5% gain
    }

    # Calculate average winner and loser
    winners = df[df['return'] > 0]['return']
    losers = df[df['return'] <= 0]['return']

    avg_winner = winners.mean() if len(winners) > 0 else 0.0
    avg_loser = losers.mean() if len(losers) > 0 else 0.0

    # Profit factor
    total_gains = winners.sum() if len(winners) > 0 else 0.0
    total_losses = abs(losers.sum()) if len(losers) > 0 else 0.0
    profit_factor = (total_gains / total_losses) if total_losses > 0 else 0.0

    return {
        "return_distribution": buckets,
        "avg_winner": round(avg_winner, 3),
        "avg_loser": round(avg_loser, 3),
        "profit_factor": round(profit_factor, 2)
    }


def prepare_trade_details(
    df: pd.DataFrame,
    entry_col: str,
    exit_col: str,
    date_col: str
) -> List[Dict[str, Any]]:

    """
    Prepare detailed trade information

    Returns:
        List of trade detail dictionaries
    """

    df = df.copy()
    df['return'] = (df[exit_col] - df[entry_col]) / df[entry_col]
    df['pnl'] = df[exit_col] - df[entry_col]

    trades = []

    for _, row in df.iterrows():
        trades.append({
            "date": str(row[date_col]) if date_col in row else "N/A",
            "entry_price": round(row[entry_col], 2),
            "exit_price": round(row[exit_col], 2),
            "return": round(row['return'], 3),
            "pnl": round(row['pnl'], 2),
            "result": "WIN" if row['return'] > 0 else "LOSS"
        })

    return trades


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    from datetime import datetime, timedelta

    # Generate sample scanner results (30 days of trades)
    np.random.seed(42)
    num_trades = 25

    dates = [datetime.now() - timedelta(days=i) for i in range(30, 0, -1)]

    # Simulate trading results
    entry_prices = np.random.uniform(100, 200, num_trades)
    returns = np.random.normal(0.01, 0.05, num_trades)  # 1% avg return, 5% std
    exit_prices = entry_prices * (1 + returns)

    scanner_results = pd.DataFrame({
        'date': dates[:num_trades],
        'ticker': np.random.choice(['AAPL', 'TSLA', 'NVDA', 'AMD', 'MSFT'], num_trades),
        'entry_price': entry_prices,
        'exit_price': exit_prices
    })

    test_input = {
        "scanner_results": scanner_results,
        "entry_price_col": "entry_price",
        "exit_price_col": "exit_price",
        "date_col": "date",
        "return_trades": True,
        "benchmark_return": 0.02
    }

    result = quick_backtester(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Quick backtest completed successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Validation Passed: {result.result['validation_passed']}")
        print(f"Total Trades: {result.result['total_trades']}")
        print(f"Win Rate: {result.result['win_rate']:.1%}")
        print(f"Total Return: {result.result['total_return']:.2%}")
        print(f"Sharpe Ratio: {result.result['sharpe_ratio']:.2f}")
        print(f"vs Benchmark: {result.result['vs_benchmark']:.2%}")
    else:
        print(f"❌ Error: {result.error}")
