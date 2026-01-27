"""
Build Plan Generator Tool

Purpose: Generate complete implementation plans for trading strategies
Version: 1.0.0
Estimated LOC: 100 lines
Target Execution: <0.5 seconds

This tool does ONE thing: Generate step-by-step build plans from strategy descriptions.
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


def build_plan_generator(input_data: Dict[str, Any]) -> ToolResult:
    """
    Generate complete implementation plan for trading strategy

    Creates a detailed, step-by-step plan for implementing a new
    trading strategy using the RENATA V2 toolset.

    Args:
        input_data: Dictionary with:
            - strategy_description (str): Strategy description [REQUIRED]
            - setup_types (list): Target setup types [REQUIRED]
            - complexity_level (str): 'simple', 'medium', 'complex' (default: 'medium')
            - include_tool_recommendations (bool): Suggest tools to use (default: True)
            - include_testing_strategy (bool): Include testing plan (default: True)
            - include_validation_checkpoints (bool): Add validation checkpoints (default: True)

    Returns:
        ToolResult with generated build plan
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
        strategy_description = input_data.get("strategy_description", "")
        setup_types = input_data.get("setup_types", [])
        complexity_level = input_data.get("complexity_level", "medium")
        include_tool_recommendations = input_data.get("include_tool_recommendations", True)
        include_testing_strategy = input_data.get("include_testing_strategy", True)
        include_validation_checkpoints = input_data.get("include_validation_checkpoints", True)

        # Analyze strategy requirements
        requirements = analyze_requirements(strategy_description, setup_types, complexity_level)

        # Generate tool recommendations
        tool_recommendations = []
        if include_tool_recommendations:
            tool_recommendations = generate_tool_recommendations(requirements)

        # Generate implementation steps
        implementation_steps = generate_implementation_steps(
            requirements,
            complexity_level,
            tool_recommendations
        )

        # Generate testing strategy
        testing_strategy = None
        if include_testing_strategy:
            testing_strategy = generate_testing_strategy(requirements, complexity_level)

        # Generate validation checkpoints
        validation_checkpoints = None
        if include_validation_checkpoints:
            validation_checkpoints = generate_validation_checkpoints(implementation_steps)

        # Calculate estimates
        estimates = calculate_estimates(requirements, complexity_level)

        # Prepare result
        result = {
            "strategy_name": generate_strategy_name(strategy_description, setup_types),
            "strategy_description": strategy_description,
            "setup_types": setup_types,
            "complexity_level": complexity_level,
            "requirements": requirements,
            "tool_recommendations": tool_recommendations,
            "implementation_steps": implementation_steps,
            "testing_strategy": testing_strategy,
            "validation_checkpoints": validation_checkpoints,
            "estimates": estimates,
            "next_steps": generate_next_steps(implementation_steps)
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
    required_fields = ["strategy_description", "setup_types"]
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

    # Validate strategy_description
    strategy_description = input_data.get("strategy_description", "")
    if not strategy_description or not isinstance(strategy_description, str):
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "strategy_description must be a non-empty string",
                "parameter": "strategy_description"
            }
        }

    # Validate setup_types
    setup_types = input_data.get("setup_types", [])
    if not isinstance(setup_types, list) or len(setup_types) == 0:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": "setup_types must be a non-empty list",
                "parameter": "setup_types"
            }
        }

    # Validate complexity_level
    complexity_level = input_data.get("complexity_level", "medium")
    valid_levels = ["simple", "medium", "complex"]
    if complexity_level not in valid_levels:
        return {
            "valid": False,
            "error": {
                "code": "INVALID_INPUT",
                "message": f"complexity_level must be one of {valid_levels}",
                "provided": complexity_level,
                "valid_options": valid_levels
            }
        }

    return {"valid": True}


def analyze_requirements(description: str, setup_types: List[str], complexity: str) -> Dict[str, Any]:
    """
    Analyze strategy requirements

    Returns:
        Dictionary with requirements analysis
    """

    # Detect required components
    has_gap_detection = any(term in description.lower() for term in ["gap", "overnight", "pre-market"])
    has_trend_detection = any(term in description.lower() for term in ["trend", "ema", "moving average"])
    has_volume_analysis = "volume" in description.lower()
    has_multi_timeframe = any(term in description.lower() for term in ["multi", "multiple", "different time"])
    has_backtesting = "backtest" in description.lower()

    # Calculate technical complexity
    technical_components = 0
    if has_gap_detection:
        technical_components += 1
    if has_trend_detection:
        technical_components += 1
    if has_volume_analysis:
        technical_components += 1
    if has_multi_timeframe:
        technical_components += 2
    if has_backtesting:
        technical_components += 1

    return {
        "has_gap_detection": has_gap_detection,
        "has_trend_detection": has_trend_detection,
        "has_volume_analysis": has_volume_analysis,
        "has_multi_timeframe": has_multi_timeframe,
        "has_backtesting": has_backtesting,
        "technical_components": technical_components,
        "data_requirements": estimate_data_requirements(setup_types, complexity)
    }


def estimate_data_requirements(setup_types: List[str], complexity: str) -> Dict[str, Any]:
    """
    Estimate data requirements

    Returns:
        Dictionary with data requirements
    """

    # Base requirements
    required_fields = ['open', 'high', 'low', 'close', 'volume']
    lookback_period = 50

    # Adjust based on setup types
    if "BACKSIDE_B" in setup_types:
        lookback_period = max(lookback_period, 89)  # Need EMA89
    if "D2" in setup_types:
        lookback_period = max(lookback_period, 20)  # Need EMA20

    # Adjust based on complexity
    if complexity == "complex":
        lookback_period *= 2

    return {
        "required_fields": required_fields,
        "lookback_period": lookback_period,
        "premarket_required": any(s in setup_types for s in ["BACKSIDE_B", "FBO", "T30"]),
        "intraday_data": any(s in setup_types for s in ["FBO", "T30", "MDR"])
    }


def generate_tool_recommendations(requirements: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generate tool recommendations

    Returns:
        List of recommended tools with reasons
    """

    recommendations = []

    # Core scanner tools (always needed)
    recommendations.append({
        "tool": "v31_scanner_generator",
        "phase": "Generation",
        "reason": "Generate V31-compliant scanner code"
    })

    recommendations.append({
        "tool": "v31_validator",
        "phase": "Validation",
        "reason": "Validate scanner meets V31 Gold Standard"
    })

    recommendations.append({
        "tool": "scanner_executor",
        "phase": "Execution",
        "reason": "Execute scanner on market data"
    })

    # Market analysis tools
    if requirements["has_trend_detection"]:
        recommendations.append({
            "tool": "indicator_calculator",
            "phase": "Analysis",
            "reason": "Calculate trend indicators (EMA clouds, etc.)"
        })

    if requirements["has_trend_detection"]:
        recommendations.append({
            "tool": "market_structure_analyzer",
            "phase": "Analysis",
            "reason": "Detect pivots, trends, support/resistance"
        })

    # Daily context detection
    if len(requirements.get("setup_types", [])) > 1:
        recommendations.append({
            "tool": "daily_context_detector",
            "phase": "Analysis",
            "reason": "Detect daily market molds for context"
        })

    # Validation tools
    recommendations.append({
        "tool": "a_plus_analyzer",
        "phase": "Validation",
        "reason": "Validate against A+ historical examples"
    })

    recommendations.append({
        "tool": "quick_backtester",
        "phase": "Validation",
        "reason": "Quick 30-day backtest validation"
    })

    # Optimization tools
    recommendations.append({
        "tool": "parameter_optimizer",
        "phase": "Optimization",
        "reason": "Optimize scanner parameters"
    })

    recommendations.append({
        "tool": "sensitivity_analyzer",
        "phase": "Optimization",
        "reason": "Test parameter sensitivity"
    })

    # Backtest tools
    if requirements["has_backtesting"]:
        recommendations.append({
            "tool": "backtest_generator",
            "phase": "Testing",
            "reason": "Generate complete backtest script"
        })

        recommendations.append({
            "tool": "backtest_analyzer",
            "phase": "Testing",
            "reason": "Analyze backtest results"
        })

    return recommendations


def generate_implementation_steps(
    requirements: Dict[str, Any],
    complexity: str,
    tool_recommendations: List[Dict[str, str]]
) -> List[Dict[str, Any]]:

    """
    Generate implementation steps

    Returns:
        List of implementation steps
    """

    steps = []

    # Step 1: Requirements Analysis
    steps.append({
        "step": 1,
        "phase": "Planning",
        "title": "Analyze Requirements",
        "description": "Document strategy requirements, setup types, and success criteria",
        "tools": [],
        "estimated_time": "1-2 hours",
        "deliverables": ["Requirements document", "Setup type definitions", "Success criteria"]
    })

    # Step 2: Generate Scanner
    steps.append({
        "step": 2,
        "phase": "Generation",
        "title": "Generate V31 Scanner",
        "description": "Create V31-compliant scanner code using v31_scanner_generator",
        "tools": ["v31_scanner_generator"],
        "estimated_time": "2-4 hours",
        "deliverables": ["Scanner code", "Validation report"]
    })

    # Step 3: Validate Scanner
    steps.append({
        "step": 3,
        "phase": "Validation",
        "title": "Validate Scanner",
        "description": "Ensure scanner meets V31 Gold Standard compliance",
        "tools": ["v31_validator"],
        "estimated_time": "0.5-1 hour",
        "deliverables": ["Validation report", "Compliance status"]
    })

    # Step 4: Market Analysis Integration
    if requirements["has_trend_detection"]:
        steps.append({
            "step": 4,
            "phase": "Analysis",
            "title": "Integrate Market Analysis",
            "description": "Add market structure and indicator analysis",
            "tools": ["indicator_calculator", "market_structure_analyzer"],
            "estimated_time": "2-3 hours",
            "deliverables": ["Enhanced scanner with analysis"]
        })

    # Step 5: Optimize Parameters
    steps.append({
        "step": len(steps) + 1,
        "phase": "Optimization",
        "title": "Optimize Parameters",
        "description": "Use parameter_optimizer to find optimal values",
        "tools": ["parameter_optimizer", "sensitivity_analyzer"],
        "estimated_time": "2-4 hours",
        "deliverables": ["Optimized parameters", "Sensitivity report"]
    })

    # Step 6: Validate on A+ Examples
    steps.append({
        "step": len(steps) + 1,
        "phase": "Validation",
        "title": "A+ Validation",
        "description": "Test scanner on historical A+ setups",
        "tools": ["a_plus_analyzer"],
        "estimated_time": "1-2 hours",
        "deliverables": ["A+ validation report", "Catch rate analysis"]
    })

    # Step 7: Quick Backtest
    steps.append({
        "step": len(steps) + 1,
        "phase": "Testing",
        "title": "Quick Backtest",
        "description": "Run 30-day quick backtest validation",
        "tools": ["quick_backtester"],
        "estimated_time": "0.5-1 hour",
        "deliverables": ["Backtest results", "Performance metrics"]
    })

    # Step 8: Full Backtest
    if requirements["has_backtesting"]:
        steps.append({
            "step": len(steps) + 1,
            "phase": "Testing",
            "title": "Full Backtest",
            "description": "Generate and run complete backtest analysis",
            "tools": ["backtest_generator", "backtest_analyzer"],
            "estimated_time": "3-5 hours",
            "deliverables": ["Backtest script", "Analysis report", "Performance metrics"]
        })

    # Step 9: Final Validation
    steps.append({
        "step": len(steps) + 1,
        "phase": "Validation",
        "title": "Final Validation",
        "description": "Comprehensive validation of all components",
        "tools": ["v31_validator", "a_plus_analyzer"],
        "estimated_time": "1-2 hours",
        "deliverables": ["Final validation report", "Readiness assessment"]
    })

    return steps


def generate_testing_strategy(requirements: Dict[str, Any], complexity: str) -> Dict[str, Any]:
    """
    Generate testing strategy

    Returns:
        Dictionary with testing strategy
    """

    # Base test cases
    test_cases = [
        "Normal operation scenarios",
        "Edge cases (boundary conditions)",
        "Error handling (missing data, invalid inputs)",
        "Performance benchmarks"
    ]

    # Add complexity-specific tests
    if complexity == "complex":
        test_cases.extend([
            "Multi-timeframe synchronization",
            "Cross-setup validation",
            "Stress testing (high data volume)"
        ])

    return {
        "test_cases": test_cases,
        "test_priority": "High" if complexity == "complex" else "Medium",
        "coverage_target": "95%",
        "performance_tests": True,
        "integration_tests": len(test_cases) > 4
    }


def generate_validation_checkpoints(implementation_steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate validation checkpoints

    Returns:
        List of validation checkpoints
    """

    checkpoints = []

    for step in implementation_steps:
        if step["phase"] in ["Validation", "Testing"]:
            checkpoints.append({
                "checkpoint": f"After {step['title']}",
                "step_number": step["step"],
                "criteria": [
                    "All deliverables completed",
                    "Tests passing",
                    "No critical bugs",
                    "Performance targets met"
                ],
                "approval_required": step["phase"] == "Validation"
            })

    return checkpoints


def calculate_estimates(requirements: Dict[str, Any], complexity: str) -> Dict[str, Any]:
    """
    Calculate time and effort estimates

    Returns:
        Dictionary with estimates
    """

    # Base hours by complexity
    base_hours = {
        "simple": 8,
        "medium": 16,
        "complex": 32
    }

    # Safely get base hours
    total_hours = base_hours.get(complexity, 16)  # Default to medium if unknown

    # Add technical components
    total_hours += requirements.get("technical_components", 0) * 2

    # Testing overhead
    testing_multiplier = 1.3
    total_hours *= testing_multiplier

    return {
        "total_hours": round(total_hours, 1),
        "total_days": round(total_hours / 8, 1),
        "development_hours": round(total_hours / 1.3, 1),
        "testing_hours": round(total_hours * 0.3 / 1.3, 1),
        "complexity": complexity
    }


def generate_strategy_name(description: str, setup_types: List[str]) -> str:
    """
    Generate strategy name from description

    Returns:
        Generated strategy name
    """

    # Extract keywords
    words = description.split()
    keywords = [w.capitalize() for w in words if len(w) > 3][:3]

    if keywords:
        base_name = "_".join(keywords)
    else:
        base_name = "CustomStrategy"

    # Add setup suffix
    if setup_types:
        setup_suffix = setup_types[0].replace("_", " ")
        return f"{base_name} ({setup_suffix})"

    return base_name


def generate_next_steps(implementation_steps: List[Dict[str, Any]]) -> List[str]:
    """
    Generate next steps

    Returns:
        List of next steps
    """

    if not implementation_steps:
        return ["Define strategy requirements"]

    first_step = implementation_steps[0]

    return [
        f"Start with: {first_step['title']}",
        f"Estimated time: {first_step['estimated_time']}",
        f"Required tools: {', '.join(first_step['tools']) if first_step['tools'] else 'None'}",
        "Review tool recommendations",
        "Set up development environment",
        "Begin implementation"
    ]


if __name__ == "__main__":
    # Test the tool
    test_input = {
        "strategy_description": "Momentum strategy that detects gap up continuations with EMA cloud confirmation and volume validation",
        "setup_types": ["BACKSIDE_B", "D2"],
        "complexity_level": "medium",
        "include_tool_recommendations": True,
        "include_testing_strategy": True,
        "include_validation_checkpoints": True
    }

    result = build_plan_generator(test_input)

    if result.status == ToolStatus.SUCCESS:
        print("✅ Build plan generated successfully!")
        print(f"Execution time: {result.execution_time:.4f}s")
        print(f"\nStrategy: {result.result['strategy_name']}")
        print(f"Complexity: {result.result['complexity_level']}")
        print(f"\nEstimates:")
        print(f"  Total Hours: {result.result['estimates']['total_hours']}")
        print(f"  Total Days: {result.result['estimates']['total_days']}")
        print(f"\nImplementation Steps: {len(result.result['implementation_steps'])}")
        print(f"Tool Recommendations: {len(result.result['tool_recommendations'])}")
        print(f"Validation Checkpoints: {len(result.result['validation_checkpoints'])}")
        print(f"\nNext Steps:")
        for step in result.result['next_steps']:
            print(f"  • {step}")
    else:
        print(f"❌ Error: {result.error}")
