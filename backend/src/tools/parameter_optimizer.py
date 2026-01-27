"""
Parameter Optimizer Tool

Purpose: Grid search optimization for scanner parameters
Version: 1.0.0
Estimated LOC: 80 lines
Target Execution: <2 seconds

This tool does ONE thing: Find optimal parameters through grid search.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List
import time
from itertools import product

# Import shared types
try:
    from .tool_types import ToolStatus, ToolResult
except ImportError:
    from tool_types import ToolStatus, ToolResult


def parameter_optimizer(input_data: Dict[str, Any]) -> ToolResult:
    """
    Optimize scanner parameters using grid search

    Tests parameter combinations and returns the best performing set.
    This is a simplified grid search focused on key parameters.

    Args:
        input_data: Dictionary with:
            - scanner_function (callable): Function that runs scanner [REQUIRED]
            - parameter_ranges (dict): Parameter ranges to test [REQUIRED]
            - evaluation_data (pd.DataFrame): Test data for evaluation [REQUIRED]
            - metric (str): Optimization metric (default: 'total_return')
            - max_iterations (int): Max combinations to test (default: 100)
            - return_all_results (bool): Return all combinations (default: False)

    Returns:
        ToolResult with optimization results
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
        scanner_function = input_data.get("scanner_function")
        parameter_ranges = input_data.get("parameter_ranges", {})
        evaluation_data = input_data.get("evaluation_data")
        metric = input_data.get("metric", "total_return")
        max_iterations = input_data.get("max_iterations", 100)
        return_all_results = input_data.get("return_all_results", False)

        # Generate parameter combinations
        combinations = generate_combinations(parameter_ranges, max_iterations)

        # Evaluate each combination
        results = []

        for params in combinations:
            try:
                # Run scanner with these parameters
                scanner_result = scanner_function(evaluation_data, **params)

                # Calculate performance metric
                performance = calculate_metric(scanner_result, metric)

                results.append({
                    "parameters": params,
                    "performance": performance,
                    "metric_value": performance.get(metric, 0.0)
                })

            except Exception as e:
                # Skip failed combinations
                continue

        # Find best parameters
        if results:
            best_result = max(results, key=lambda x: x["metric_value"])
        else:
            best_result = {
                "parameters": {},
                "performance": {},
                "metric_value": 0.0
            }

        # Calculate optimization statistics
        optimization_stats = calculate_optimization_stats(results, metric)

        # Prepare result
        result = {
            "best_parameters": best_result["parameters"],
            "best_performance": best_result["performance"],
            "best_metric_value": round(best_result["metric_value"], 4),
            "optimization_metric": metric,
            "combinations_tested": len(results),
            "optimization_stats": optimization_stats,
            "all_results": results if return_all_results else []
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
    required_fields = ["parameter_ranges", "evaluation_data"]
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

    # Validate parameter_ranges
    parameter_ranges = input_data.get("parameter_ranges", {})
    if not isinstance(parameter_ranges, dict) or len(parameter_ranges) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "parameter_ranges must be a non-empty dict",
                "parameter": "parameter_ranges"
            }
        }

    # Validate evaluation_data
    evaluation_data = input_data.get("evaluation_data")
    if evaluation_data is None or not isinstance(evaluation_data, pd.DataFrame):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_TYPE",
                "message": "evaluation_data must be a pandas DataFrame",
                "parameter": "evaluation_data"
            }
        }

    if len(evaluation_data) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INSUFFICIENT_DATA",
                "message": "evaluation_data is empty",
                "minimum_required": 1
            }
        }

    return {"valid": True}


def generate_combinations(parameter_ranges: Dict[str, List], max_iterations: int) -> List[Dict[str, Any]]:
    """
    Generate parameter combinations for grid search

    Returns:
        List of parameter dictionaries
    """

    # Convert parameter ranges to lists of values
    param_names = list(parameter_ranges.keys())
    param_values = [parameter_ranges[name] for name in param_names]

    # Generate all combinations
    all_combinations = list(product(*param_values))

    # Limit to max_iterations
    if len(all_combinations) > max_iterations:
        # Sample random combinations
        indices = np.random.choice(len(all_combinations), max_iterations, replace=False)
        all_combinations = [all_combinations[i] for i in indices]

    # Convert to list of dicts
    combinations = []
    for combo in all_combinations:
        param_dict = dict(zip(param_names, combo))
        combinations.append(param_dict)

    return combinations


def calculate_metric(scanner_result: Any, metric: str) -> Dict[str, float]:
    """
    Calculate performance metric from scanner result

    Returns:
        Dictionary with calculated metrics
    """

    # This is a simplified implementation
    # In production, you'd extract actual metrics from scanner_result

    if isinstance(scanner_result, pd.DataFrame):
        if len(scanner_result) == 0:
            return {
                "total_return": 0.0,
                "win_rate": 0.0,
                "sharpe_ratio": 0.0
            }

        # Calculate basic metrics
        if 'return' in scanner_result.columns:
            returns = scanner_result['return']
            total_return = returns.sum()
            win_rate = (returns > 0).sum() / len(returns)

            if len(returns) > 1:
                sharpe_ratio = returns.mean() / returns.std() if returns.std() > 0 else 0.0
            else:
                sharpe_ratio = 0.0

            return {
                "total_return": total_return,
                "win_rate": win_rate,
                "sharpe_ratio": sharpe_ratio
            }
        else:
            # Fallback: count results as proxy for performance
            return {
                "total_return": len(scanner_result) / 100.0,  # Normalized
                "win_rate": 0.5,
                "sharpe_ratio": 0.0
            }
    else:
        # Non-DataFrame result: return default metrics
        return {
            "total_return": 0.0,
            "win_rate": 0.0,
            "sharpe_ratio": 0.0
        }


def calculate_optimization_stats(results: List[Dict[str, Any]], metric: str) -> Dict[str, Any]:
    """
    Calculate optimization statistics

    Returns:
        Dictionary with optimization statistics
    """

    if not results:
        return {
            "mean_metric_value": 0.0,
            "std_metric_value": 0.0,
            "min_metric_value": 0.0,
            "max_metric_value": 0.0
        }

    metric_values = [r["metric_value"] for r in results]

    return {
        "mean_metric_value": round(np.mean(metric_values), 4),
        "std_metric_value": round(np.std(metric_values), 4),
        "min_metric_value": round(np.min(metric_values), 4),
        "max_metric_value": round(np.max(metric_values), 4)
    }


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np

    # Sample scanner function
    def sample_scanner(df, gap_threshold=0.8, volume_multiplier=1.5):
        """Sample scanner that filters based on parameters"""

        # Simple filtering logic
        mask = (
            (df.get('gap_over_atr', 0) > gap_threshold) &
            (df.get('volume_ratio', 1) > volume_multiplier)
        )

        results = df[mask]

        # Add synthetic return column
        if len(results) > 0:
            np.random.seed(42)
            results = results.copy()
            results['return'] = np.random.normal(0.02, 0.05, len(results))

        return results

    # Sample evaluation data
    np.random.seed(42)
    evaluation_data = pd.DataFrame({
        'gap_over_atr': np.random.uniform(0, 2, 100),
        'volume_ratio': np.random.uniform(0.5, 3, 100),
        'ticker': [f'STOCK{i}' for i in range(100)]
    })

    test_input = {
        "scanner_function": sample_scanner,
        "parameter_ranges": {
            "gap_threshold": [0.5, 0.8, 1.0, 1.2],
            "volume_multiplier": [1.0, 1.5, 2.0]
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "max_iterations": 50
    }

    result = parameter_optimizer(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Parameter optimization completed successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Best Parameters: {result.result['best_parameters']}")
        print(f"Best {result.result['optimization_metric']}: {result.result['best_metric_value']:.4f}")
        print(f"Combinations Tested: {result.result['combinations_tested']}")
        print(f"Mean Performance: {result.result['optimization_stats']['mean_metric_value']:.4f}")
    else:
        print(f"❌ Error: {result.error}")
