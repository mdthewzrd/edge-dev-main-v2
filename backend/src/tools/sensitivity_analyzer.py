"""
Sensitivity Analyzer Tool

Purpose: Test parameter sensitivity and robustness
Version: 1.0.0
Estimated LOC: 60 lines
Target Execution: <1 second

This tool does ONE thing: Analyze how sensitive results are to parameter changes.
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


def sensitivity_analyzer(input_data: Dict[str, Any]) -> ToolResult:
    """
    Analyze parameter sensitivity and robustness

    Tests how scanner performance changes with small parameter variations.
    Identifies robust vs fragile parameters.

    Args:
        input_data: Dictionary with:
            - scanner_function (callable): Function that runs scanner [REQUIRED]
            - base_parameters (dict): Base parameter values [REQUIRED]
            - parameter_variations (dict): Variations to test (+/- %) [REQUIRED]
            - evaluation_data (pd.DataFrame): Test data for evaluation [REQUIRED]
            - sensitivity_threshold (float): Threshold for "sensitive" (default: 0.2)
            - metric (str): Performance metric to analyze (default: 'total_return')

    Returns:
        ToolResult with sensitivity analysis
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
        base_parameters = input_data.get("base_parameters", {})
        parameter_variations = input_data.get("parameter_variations", {})
        evaluation_data = input_data.get("evaluation_data")
        sensitivity_threshold = input_data.get("sensitivity_threshold", 0.2)
        metric = input_data.get("metric", "total_return")

        # Calculate base performance
        base_result = scanner_function(evaluation_data, **base_parameters)
        base_performance = calculate_metric(base_result, metric)
        base_metric_value = base_performance.get(metric, 0.0)

        # Test variations for each parameter
        sensitivity_results = []

        for param_name, variation_pct in parameter_variations.items():
            if param_name not in base_parameters:
                continue

            base_value = base_parameters[param_name]

            # Test +variation
            params_plus = base_parameters.copy()
            params_plus[param_name] = base_value * (1 + variation_pct / 100.0)

            result_plus = scanner_function(evaluation_data, **params_plus)
            performance_plus = calculate_metric(result_plus, metric)
            metric_plus = performance_plus.get(metric, 0.0)

            # Test -variation
            params_minus = base_parameters.copy()
            params_minus[param_name] = base_value * (1 - variation_pct / 100.0)

            result_minus = scanner_function(evaluation_data, **params_minus)
            performance_minus = calculate_metric(result_minus, metric)
            metric_minus = performance_minus.get(metric, 0.0)

            # Calculate sensitivity
            change_plus = abs(metric_plus - base_metric_value)
            change_minus = abs(metric_minus - base_metric_value)
            max_change = max(change_plus, change_minus)

            # Normalize sensitivity
            if base_metric_value != 0:
                normalized_sensitivity = max_change / abs(base_metric_value)
            else:
                normalized_sensitivity = 0.0

            # Classify sensitivity
            if normalized_sensitivity > sensitivity_threshold:
                sensitivity_level = "HIGH"
            elif normalized_sensitivity > sensitivity_threshold / 2:
                sensitivity_level = "MEDIUM"
            else:
                sensitivity_level = "LOW"

            sensitivity_results.append({
                "parameter": param_name,
                "base_value": base_value,
                "variation_pct": variation_pct,
                "metric_plus": round(metric_plus, 4),
                "metric_minus": round(metric_minus, 4),
                "change_plus": round(change_plus, 4),
                "change_minus": round(change_minus, 4),
                "max_change": round(max_change, 4),
                "normalized_sensitivity": round(normalized_sensitivity, 4),
                "sensitivity_level": sensitivity_level
            })

        # Identify sensitive parameters
        sensitive_params = [
            r for r in sensitivity_results
            if r["sensitivity_level"] in ["HIGH", "MEDIUM"]
        ]

        # Calculate robustness score
        robust_params = len([r for r in sensitivity_results if r["sensitivity_level"] == "LOW"])
        robustness_score = robust_params / len(sensitivity_results) if sensitivity_results else 0.0

        # Prepare result
        result = {
            "base_metric_value": round(base_metric_value, 4),
            "metric": metric,
            "sensitivity_threshold": sensitivity_threshold,
            "sensitivity_results": sensitivity_results,
            "sensitive_parameters": len(sensitive_params),
            "robust_parameters": robust_params,
            "robustness_score": round(robustness_score, 4),
            "recommendation": generate_recommendation(sensitivity_results, robustness_score)
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
    required_fields = ["base_parameters", "parameter_variations", "evaluation_data"]
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

    # Validate base_parameters
    base_parameters = input_data.get("base_parameters", {})
    if not isinstance(base_parameters, dict) or len(base_parameters) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "base_parameters must be a non-empty dict",
                "parameter": "base_parameters"
            }
        }

    # Validate parameter_variations
    parameter_variations = input_data.get("parameter_variations", {})
    if not isinstance(parameter_variations, dict) or len(parameter_variations) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "parameter_variations must be a non-empty dict",
                "parameter": "parameter_variations"
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


def calculate_metric(scanner_result: Any, metric: str) -> Dict[str, float]:
    """
    Calculate performance metric from scanner result

    Returns:
        Dictionary with calculated metrics
    """

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
            # Fallback: count results
            return {
                "total_return": len(scanner_result) / 100.0,
                "win_rate": 0.5,
                "sharpe_ratio": 0.0
            }
    else:
        return {
            "total_return": 0.0,
            "win_rate": 0.0,
            "sharpe_ratio": 0.0
        }


def generate_recommendation(sensitivity_results: List[Dict[str, Any]], robustness_score: float) -> str:
    """
    Generate recommendation based on sensitivity analysis

    Returns:
        Recommendation string
    """

    if robustness_score >= 0.7:
        return "Parameters are robust. Scanner performs consistently across variations."
    elif robustness_score >= 0.4:
        sensitive_params = [r["parameter"] for r in sensitivity_results if r["sensitivity_level"] == "HIGH"]
        return f"Moderate sensitivity. Consider fine-tuning: {', '.join(sensitive_params)}"
    else:
        sensitive_params = [r["parameter"] for r in sensitivity_results if r["sensitivity_level"] in ["HIGH", "MEDIUM"]]
        return f"High sensitivity. Scanner is fragile. Focus on: {', '.join(sensitive_params)}"


if __name__ == "__main__":
    # Test the tool
    import pandas as pd
    import numpy as np

    # Sample scanner function
    def sample_scanner(df, gap_threshold=0.8, volume_multiplier=1.5):
        """Sample scanner that filters based on parameters"""

        mask = (
            (df.get('gap_over_atr', 0) > gap_threshold) &
            (df.get('volume_ratio', 1) > volume_multiplier)
        )

        results = df[mask]

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
        "base_parameters": {
            "gap_threshold": 0.8,
            "volume_multiplier": 1.5
        },
        "parameter_variations": {
            "gap_threshold": 20,  # Test +/- 20%
            "volume_multiplier": 20
        },
        "evaluation_data": evaluation_data,
        "metric": "total_return",
        "sensitivity_threshold": 0.2
    }

    result = sensitivity_analyzer(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Sensitivity analysis completed successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"Base {result.result['metric']}: {result.result['base_metric_value']:.4f}")
        print(f"Robustness Score: {result.result['robustness_score']:.2%}")
        print(f"Sensitive Parameters: {result.result['sensitive_parameters']}")
        print(f"Recommendation: {result.result['recommendation']}")
        print("\nParameter Sensitivity:")
        for r in result.result['sensitivity_results']:
            print(f"  {r['parameter']}: {r['sensitivity_level']} sensitivity (max change: {r['max_change']:.4f})")
    else:
        print(f"❌ Error: {result.error}")
