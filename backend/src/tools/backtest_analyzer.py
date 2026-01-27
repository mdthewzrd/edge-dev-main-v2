"""
Backtest Analyzer Tool

Purpose: Analyze backtest results and generate detailed metrics
Version: 1.0.0
Estimated LOC: 80 lines
Target Execution: <1 second

This tool does ONE thing: Analyze backtest results and metrics.
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


def backtest_analyzer(input_data: Dict[str, Any]) -> ToolResult:
    """
    Analyze backtest results and generate detailed metrics

    Calculates comprehensive performance metrics from backtest results
    including risk-adjusted returns, drawdown analysis, and trade statistics.

    Args:
        input_data: Dictionary with:
            - backtest_results (pd.DataFrame): Backtest trade results [REQUIRED]
            - initial_capital (float): Starting capital (default: 100000)
            - benchmark_return (float): Benchmark return for comparison (default: 0.10)
            - include_drawdown_analysis (bool): Calculate drawdown metrics (default: True)
            - include_trade_stats (bool): Calculate trade statistics (default: True)
            - risk_free_rate (float): Risk-free rate for Sharpe (default: 0.02)

    Returns:
        ToolResult with backtest analysis metrics
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
        backtest_results = input_data.get("backtest_results")
        initial_capital = input_data.get("initial_capital", 100000)
        benchmark_return = input_data.get("benchmark_return", 0.10)
        include_drawdown_analysis = input_data.get("include_drawdown_analysis", True)
        include_trade_stats = input_data.get("include_trade_stats", True)
        risk_free_rate = input_data.get("risk_free_rate", 0.02)

        # Calculate return metrics
        return_metrics = calculate_return_metrics(backtest_results, initial_capital)

        # Calculate risk metrics
        risk_metrics = calculate_risk_metrics(backtest_results, risk_free_rate)

        # Calculate drawdown analysis
        drawdown_metrics = {}
        if include_drawdown_analysis:
            drawdown_metrics = calculate_drawdown_analysis(backtest_results, initial_capital)

        # Calculate trade statistics
        trade_stats = {}
        if include_trade_stats:
            trade_stats = calculate_trade_statistics(backtest_results)

        # Calculate benchmark comparison
        benchmark_comparison = calculate_benchmark_comparison(
            return_metrics,
            benchmark_return
        )

        # Calculate overall score
        overall_score = calculate_overall_score(
            return_metrics,
            risk_metrics,
            drawdown_metrics
        )

        # Prepare result
        result = {
            "return_metrics": return_metrics,
            "risk_metrics": risk_metrics,
            "drawdown_analysis": drawdown_metrics,
            "trade_statistics": trade_stats,
            "benchmark_comparison": benchmark_comparison,
            "overall_score": round(overall_score, 2),
            "initial_capital": initial_capital,
            "final_capital": round(return_metrics["final_capital"], 2),
            "analysis_summary": generate_summary(
                return_metrics,
                risk_metrics,
                drawdown_metrics,
                overall_score
            )
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
    required_fields = ["backtest_results"]
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

    # Validate backtest_results
    backtest_results = input_data.get("backtest_results")
    if backtest_results is None:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "backtest_results cannot be None",
                "parameter": "backtest_results"
            }
        }

    # Check if it's a DataFrame
    if not isinstance(backtest_results, pd.DataFrame):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "backtest_results must be a pandas DataFrame",
                "parameter": "backtest_results"
            }
        }

    # Check for data FIRST (before checking columns)
    if len(backtest_results) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INSUFFICIENT_DATA",
                "message": "backtest_results is empty",
                "minimum_required": 1
            }
        }

    # Check for required columns
    required_cols = ['return']
    missing_cols = [col for col in required_cols if col not in backtest_results.columns]

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


def calculate_return_metrics(df: pd.DataFrame, initial_capital: float) -> Dict[str, Any]:
    """
    Calculate return metrics

    Returns:
        Dictionary with return metrics
    """

    total_return = df['return'].sum()
    final_capital = initial_capital * (1 + total_return)

    # Calculate cumulative returns
    cumulative_returns = (1 + df['return']).cumprod()
    total_cumulative_return = cumulative_returns.iloc[-1] - 1

    # Calculate best and worst trades
    best_trade = df['return'].max()
    worst_trade = df['return'].min()

    # Calculate average return
    avg_return = df['return'].mean()

    return {
        "total_return": round(total_return, 4),
        "total_cumulative_return": round(total_cumulative_return, 4),
        "final_capital": round(final_capital, 2),
        "best_trade": round(best_trade, 4),
        "worst_trade": round(worst_trade, 4),
        "avg_return": round(avg_return, 4)
    }


def calculate_risk_metrics(df: pd.DataFrame, risk_free_rate: float) -> Dict[str, Any]:
    """
    Calculate risk metrics

    Returns:
        Dictionary with risk metrics
    """

    returns = df['return']

    # Win rate
    win_rate = (returns > 0).sum() / len(returns)

    # Standard deviation
    std_dev = returns.std()

    # Sharpe ratio (simplified)
    excess_return = returns.mean() - risk_free_rate / 252  # Daily risk-free
    sharpe_ratio = (returns.mean() / std_dev) if std_dev > 0 else 0.0

    # Sortino ratio (downside deviation)
    downside_returns = returns[returns < 0]
    downside_deviation = downside_returns.std() if len(downside_returns) > 0 else 0.001
    sortino_ratio = (returns.mean() / downside_deviation) if downside_deviation > 0 else 0.0

    # Calmar ratio (return / max drawdown) - will be updated with drawdown
    calmar_ratio = 0.0  # Placeholder

    return {
        "win_rate": round(win_rate, 4),
        "std_dev": round(std_dev, 4),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "sortino_ratio": round(sortino_ratio, 2),
        "calmar_ratio": round(calmar_ratio, 2)
    }


def calculate_drawdown_analysis(df: pd.DataFrame, initial_capital: float) -> Dict[str, Any]:
    """
    Calculate drawdown analysis

    Returns:
        Dictionary with drawdown metrics
    """

    # Calculate cumulative returns
    cumulative_returns = (1 + df['return']).cumprod()
    equity_curve = initial_capital * cumulative_returns

    # Calculate running maximum
    running_max = equity_curve.cummax()

    # Calculate drawdown
    drawdown = (equity_curve - running_max) / running_max

    # Maximum drawdown
    max_drawdown = drawdown.min()

    # Average drawdown
    avg_drawdown = drawdown[drawdown < 0].mean() if (drawdown < 0).any() else 0.0

    # Drawdown duration
    in_drawdown = drawdown < 0
    drawdown_periods = []
    current_drawdown = False
    drawdown_start = 0

    for i, is_dd in enumerate(in_drawdown):
        if is_dd and not current_drawdown:
            current_drawdown = True
            drawdown_start = i
        elif not is_dd and current_drawdown:
            current_drawdown = False
            drawdown_periods.append(i - drawdown_start)

    max_drawdown_duration = max(drawdown_periods) if drawdown_periods else 0
    avg_drawdown_duration = np.mean(drawdown_periods) if drawdown_periods else 0.0

    return {
        "max_drawdown": round(max_drawdown, 4),
        "avg_drawdown": round(avg_drawdown, 4),
        "max_drawdown_duration": int(max_drawdown_duration),
        "avg_drawdown_duration": round(avg_drawdown_duration, 1)
    }


def calculate_trade_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate trade statistics

    Returns:
        Dictionary with trade statistics
    """

    returns = df['return']

    # Number of trades
    total_trades = len(returns)
    winning_trades = (returns > 0).sum()
    losing_trades = (returns <= 0).sum()

    # Average winner and loser
    avg_winner = returns[returns > 0].mean() if winning_trades > 0 else 0.0
    avg_loser = returns[returns <= 0].mean() if losing_trades > 0 else 0.0

    # Profit factor
    total_profits = returns[returns > 0].sum() if winning_trades > 0 else 0.0
    total_losses = abs(returns[returns <= 0].sum()) if losing_trades > 0 else 0.0
    profit_factor = (total_profits / total_losses) if total_losses > 0 else 0.0

    # Largest winner and loser
    largest_winner = returns[returns > 0].max() if winning_trades > 0 else 0.0
    largest_loser = returns[returns <= 0].min() if losing_trades > 0 else 0.0

    return {
        "total_trades": int(total_trades),
        "winning_trades": int(winning_trades),
        "losing_trades": int(losing_trades),
        "avg_winner": round(avg_winner, 4),
        "avg_loser": round(avg_loser, 4),
        "profit_factor": round(profit_factor, 2),
        "largest_winner": round(largest_winner, 4),
        "largest_loser": round(largest_loser, 4)
    }


def calculate_benchmark_comparison(return_metrics: Dict[str, Any], benchmark_return: float) -> Dict[str, Any]:
    """
    Calculate benchmark comparison

    Returns:
        Dictionary with benchmark comparison
    """

    strategy_return = return_metrics["total_return"]
    excess_return = strategy_return - benchmark_return

    # Calculate information ratio (simplified)
    tracking_error = abs(excess_return) * 0.1  # Simplified
    information_ratio = (excess_return / tracking_error) if tracking_error > 0 else 0.0

    return {
        "strategy_return": round(strategy_return, 4),
        "benchmark_return": round(benchmark_return, 4),
        "excess_return": round(excess_return, 4),
        "tracking_error": round(tracking_error, 4),
        "information_ratio": round(information_ratio, 2)
    }


def calculate_overall_score(
    return_metrics: Dict[str, Any],
    risk_metrics: Dict[str, Any],
    drawdown_metrics: Dict[str, Any]
) -> float:

    """
    Calculate overall backtest score (0-100)

    Returns:
        Overall score
    """

    score = 0.0

    # Return score (40 points)
    total_return = return_metrics["total_return"]
    if total_return > 0.5:  # >50% return
        score += 40
    elif total_return > 0.3:  # >30% return
        score += 30
    elif total_return > 0.1:  # >10% return
        score += 20
    elif total_return > 0:
        score += 10

    # Risk score (30 points)
    sharpe_ratio = risk_metrics["sharpe_ratio"]
    if sharpe_ratio > 2.0:
        score += 30
    elif sharpe_ratio > 1.0:
        score += 20
    elif sharpe_ratio > 0.5:
        score += 10

    # Drawdown score (20 points)
    if drawdown_metrics:
        max_dd = abs(drawdown_metrics["max_drawdown"])
        if max_dd < 0.1:  # <10% drawdown
            score += 20
        elif max_dd < 0.2:  # <20% drawdown
            score += 15
        elif max_dd < 0.3:  # <30% drawdown
            score += 10

    # Win rate score (10 points)
    win_rate = risk_metrics["win_rate"]
    if win_rate > 0.6:
        score += 10
    elif win_rate > 0.5:
        score += 7
    elif win_rate > 0.4:
        score += 5

    return min(score, 100.0)  # Cap at 100


def generate_summary(
    return_metrics: Dict[str, Any],
    risk_metrics: Dict[str, Any],
    drawdown_metrics: Dict[str, Any],
    overall_score: float
) -> str:

    """
    Generate analysis summary

    Returns:
        Summary string
    """

    summary_parts = []

    # Overall assessment
    if overall_score >= 80:
        summary_parts.append("Excellent backtest performance.")
    elif overall_score >= 60:
        summary_parts.append("Good backtest performance.")
    elif overall_score >= 40:
        summary_parts.append("Moderate backtest performance.")
    else:
        summary_parts.append("Poor backtest performance.")

    # Return assessment
    total_return = return_metrics["total_return"]
    if total_return > 0.3:
        summary_parts.append(f"Strong returns ({total_return:.1%}).")
    elif total_return > 0:
        summary_parts.append(f"Positive returns ({total_return:.1%}).")
    else:
        summary_parts.append(f"Negative returns ({total_return:.1%}).")

    # Risk assessment
    max_dd = abs(drawdown_metrics.get("max_drawdown", 0))
    if max_dd < 0.15:
        summary_parts.append("Low risk drawdown.")
    elif max_dd < 0.25:
        summary_parts.append("Moderate risk drawdown.")
    else:
        summary_parts.append("High risk drawdown.")

    # Win rate assessment
    win_rate = risk_metrics["win_rate"]
    if win_rate > 0.6:
        summary_parts.append(f"Strong win rate ({win_rate:.1%}).")
    elif win_rate > 0.4:
        summary_parts.append(f"Moderate win rate ({win_rate:.1%}).")
    else:
        summary_parts.append(f"Weak win rate ({win_rate:.1%}).")

    return " ".join(summary_parts)


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np

    # Generate sample backtest results
    np.random.seed(42)
    num_trades = 50

    returns = np.random.normal(0.02, 0.08, num_trades)  # 2% avg return, 8% std

    backtest_results = pd.DataFrame({
        'ticker': [f'STOCK{i}' for i in range(num_trades)],
        'entry_price': np.random.uniform(100, 200, num_trades),
        'exit_price': np.random.uniform(100, 200, num_trades),
        'return': returns
    })

    test_input = {
        "backtest_results": backtest_results,
        "initial_capital": 100000,
        "benchmark_return": 0.10,
        "include_drawdown_analysis": True,
        "include_trade_stats": True
    }

    result = backtest_analyzer(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Backtest analysis completed successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Overall Score: {result.result['overall_score']}/100")
        print(f"Total Return: {result.result['return_metrics']['total_return']:.2%}")
        print(f"Sharpe Ratio: {result.result['risk_metrics']['sharpe_ratio']:.2f}")
        print(f"Win Rate: {result.result['risk_metrics']['win_rate']:.1%}")
        print(f"Max Drawdown: {result.result['drawdown_analysis']['max_drawdown']:.2%}")
        print(f"\nSummary: {result.result['analysis_summary']}")
    else:
        print(f"❌ Error: {result.error}")
